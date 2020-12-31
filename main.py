import subprocess
import pandas as pd
from datetime import datetime
import time


def main():
    # intervals in minutes that logs should be taken after restart
    intervals = [0, 5, 10, 15, 30]

    # get start time
    time_start = datetime.now()

    # Create logs
    for minutes in intervals:
        # sleep for interval
        time.sleep(minutes * 60)

        # create log
        create_log(int((datetime.now() - time_start).total_seconds() / 60))


def create_log(runtime):
    print(runtime)
    # get GPU info through nvidia-smi
    sp = subprocess.Popen(['nvidia-smi', '-q'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_str = sp.communicate()

    # split returned string into seperate lines
    out_list = str(out_str[0]).split('\\n')

    # remove \r from line-ends
    for line in out_list:
        out_list[out_list.index(line)] = str(out_list.index(line)) + " " + line[:-2]

    # parse gpu information
    graphics_clock = int((out_list[161].split(":")[-1].strip()).split(" ")[0])

    # gpu_usage = float((out_list[85].split(":")[-1])[1])/100.0
    gpu_usage = out_list[85].split(":")[-1].replace(" ", "")
    compute_mode = out_list[83].split(":")[-1]
    driver_version = float(out_list[4].split(":")[-1])
    cuda_version = float(out_list[5].split(":")[-1])
    vbios_version = out_list[25].split(":")[-1]

    # parse clock throttling reason flags
    trf_idle = out_list[66].split(":")[-1]
    trf_application_clocks_settings = out_list[67].split(":")[-1]
    trf_sw_power_cap = out_list[68].split(":")[-1]
    trf_hw_slowdown = out_list[69].split(":")[-1]
    trf_hw_thermal_slowdown = out_list[70].split(":")[-1]
    trf_hw_power_brake_slowdown = out_list[71].split(":")[-1]
    trf_sync_boost = out_list[72].split(":")[-1]
    trf_sw_thermal_slowdown = out_list[73].split(":")[-1]
    trf_display_clock_setting = out_list[74].split(":")[-1]

    # save data into dic to store as row in pandas dataframe
    new_row = {'date & time': datetime.now().strftime("%d/%m/%Y %H:%M"), 'runtime (minutes)': runtime,
               'graphics clocks (MHz)': graphics_clock, 'gpu usage': gpu_usage, 'compute mode': compute_mode,
               'driver version': driver_version, 'cuda version': cuda_version, 'vbios version': vbios_version,
               'idle': trf_idle, 'application clocks settings': trf_application_clocks_settings,
               'sw power cap': trf_sw_power_cap, 'hw slowdown': trf_hw_slowdown,
               'hw thermal slowdown': trf_hw_thermal_slowdown, 'hw power break slowdown': trf_hw_power_brake_slowdown,
               'sync boost': trf_sync_boost, 'sw thermal slowdown': trf_sw_thermal_slowdown,
               'display clock setting': trf_display_clock_setting}

    # load stored logs with pandas from excel xlsx
    df = pd.read_excel('gpu_startup_clocks.xlsx')

    # append row to the dataframe
    df = df.append(new_row, ignore_index=True)

    # save pandas dataframe back to excel file without indexes
    df.to_excel('gpu_startup_clocks.xlsx', index=False)

    print_df(df)


def print_df(df):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    print(df)


if __name__ == "__main__":
    main()
