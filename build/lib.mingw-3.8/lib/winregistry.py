import winreg
import re

# https://stackoverflow.com/a/64513550/14820021
class WindowsRegistry:
    """Class WindowsRegistry is using for easy manipulating Windows registry.


    Methods
    -------
    query_value(full_path : str)
        Check value for existing.

    get_value(full_path : str)
        Get value's data.

    set_value(full_path : str, value : str, value_type='REG_SZ' : str)
        Create a new value with data or set data to an existing value.

    delete_value(full_path : str)
        Delete an existing value.

    query_key(full_path : str)
        Check key for existing.

    delete_key(full_path : str)
        Delete an existing key(only without subkeys).


    Examples:
        WindowsRegistry.set_value('HKCU/Software/Microsoft/Windows/CurrentVersion/Run', 'Program', r'"c:\Dir1\program.exe"')
        WindowsRegistry.delete_value('HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/Run/Program')
    """
    @staticmethod
    def __parse_data(full_path):
        full_path = re.sub(r'/', r'\\', full_path)
        hive = re.sub(r'\\.*$', '', full_path)
        if not hive:
            raise ValueError('Invalid \'full_path\' param.')
        if len(hive) <= 4:
            if hive == 'HKLM':
                hive = 'HKEY_LOCAL_MACHINE'
            elif hive == 'HKCU':
                hive = 'HKEY_CURRENT_USER'
            elif hive == 'HKCR':
                hive = 'HKEY_CLASSES_ROOT'
            elif hive == 'HKU':
                hive = 'HKEY_USERS'
        reg_key = re.sub(r'^[A-Z_]*\\', '', full_path)
        reg_key = re.sub(r'\\[^\\]+$', '', reg_key)
        reg_value = re.sub(r'^.*\\', '', full_path)

        return hive, reg_key, reg_value

    @staticmethod
    def query_value(full_path):
        value_list = WindowsRegistry.__parse_data(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
            winreg.QueryValueEx(opened_key, value_list[2])
            winreg.CloseKey(opened_key)
            return True
        except WindowsError:
            return False

    @staticmethod
    def get_value(full_path):
        value_list = WindowsRegistry.__parse_data(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
            value_of_value, value_type = winreg.QueryValueEx(opened_key, value_list[2])
            winreg.CloseKey(opened_key)
            return value_of_value
        except WindowsError:
            return None

    @staticmethod
    def set_value(full_path, value, value_type='REG_SZ'):
        value_list = WindowsRegistry.__parse_data(full_path)
        try:
            winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1])
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
            winreg.SetValueEx(opened_key, value_list[2], 0, getattr(winreg, value_type), value)
            winreg.CloseKey(opened_key)
            return True
        except WindowsError:
            return False

    @staticmethod
    def delete_value(full_path):
        value_list = WindowsRegistry.__parse_data(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
            winreg.DeleteValue(opened_key, value_list[2])
            winreg.CloseKey(opened_key)
            return True
        except WindowsError:
            return False

    @staticmethod
    def query_key(full_path):
        value_list = WindowsRegistry.__parse_data(full_path)
        try:
            opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2], 0, winreg.KEY_READ)
            winreg.CloseKey(opened_key)
            return True
        except WindowsError:
            return False

    @staticmethod
    def delete_key(full_path):
        value_list = WindowsRegistry.__parse_data(full_path)
        try:
            winreg.DeleteKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
            return True
        except WindowsError:
            return False