from fman import DirectoryPaneCommand, show_status_message, clipboard, show_alert
from fman.url import as_human_readable
import os


def is_path_at_drive(path):
    drive, path_without_drive = os.path.splitdrive(path)
    return (path_without_drive == '\\')


class CopyNextcloudPathToClipboard(DirectoryPaneCommand):
    '''
    Find out if the path of the file under the cursor is within Nextcloud.
    If it is part of Nextcloud, a Nextcloud path is created and copied in the clipboard.
    '''
    def __call__(self):
        file_under_cursor = self.pane.get_file_under_cursor()
        if file_under_cursor:
            file_under_cursor = as_human_readable(file_under_cursor)
            nextcloud_path = ''

            # Is Nextcloud in the path?
            search_index = file_under_cursor.find('Nextcloud')
            if search_index != -1:
                nextcloud_path = file_under_cursor[search_index:]
            # Is the Nextcloud database in the path?
            else:
                nextcloud_db_found = False
                directory = os.path.dirname(file_under_cursor)
                while True:
                    for file in os.listdir(directory):
                        if '._sync_' in file:
                            nextcloud_db_found = True
                            break
                    if nextcloud_db_found or is_path_at_drive(directory):
                        break
                    directory = os.path.normpath(os.path.join(directory, '..'))

                if nextcloud_db_found:
                    nextcloud_directory_name = os.path.basename(directory)
                    nextcloud_path_without_root = file_under_cursor[len(directory) + 1:]
                    nextcloud_path = os.path.join('Nextcloud', nextcloud_directory_name, nextcloud_path_without_root)

            if nextcloud_path:
                clipboard.clear()
                clipboard.set_text(nextcloud_path)
                show_status_message(f'Copied "{nextcloud_path}" to the clipboard.', timeout_secs=3)