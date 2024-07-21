import sys
from resources.QuakeLog import QuakeLog

def main():
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <file_path> <report_type>")
        return

    file_path = sys.argv[1]
    report = sys.argv[2]

    quake_log = QuakeLog()

    try:
        log_list = quake_log.read_file(file_path)
        quake_log.extract_informations(log_list)

        if report == 'game_statistics':
           report = quake_log.generate_game_report()
        elif report == 'death_statistics':
            report = quake_log.generate_kill_by_means_report()
        else:
            raise ValueError(f"Unsupported report type: '{report}'")

        print(report)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()