First, export Miranda logs using Message Export plugin from http://sourceforge.net/projects/msg-export
Use following format for file name in Message Export's 'Default' field: %UIN%\%year%-%month%-%day%.txt

Second, run this tool:

     migrate_icq.py <root_dir_with_icq_logs> <target_dir_with_pidgin_icq_logs> [encoding]


