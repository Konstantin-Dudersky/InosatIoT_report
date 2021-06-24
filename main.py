import datetime
import inspect
import json
import pathlib

import pandas as pd
from influxdb_client import InfluxDBClient
import os


# read settings
with open(os.getenv('inosatiot_cfg')) as f:
    cfg = json.loads(f.read())


def report_test():
    NAME_FOR_USER = "Отчет о потреблении ЭЭ по группам нагрузок"
    TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # region setup
    output_full_path = cfg['report']['output_path'] + "/" + NAME_FOR_USER + "/" + TIMESTAMP
    output_file_name = output_full_path + "/ " + NAME_FOR_USER + "_" + TIMESTAMP
    name_internal = inspect.currentframe().f_code.co_name

    pathlib.Path(output_full_path).mkdir(parents=True, exist_ok=True)
    #distutils.dir_util.copy_tree("templates/_base", output_full_path + "/tmp")
    # distutils.file_util.copy_file("templates/" + name_internal + ".html",
    #                               output_full_path + "/tmp")
    # endregion

    query = """
    counterByTime = (table =<-, every) =>
      table
        |> window(every: every, createEmpty: true)
        |> increase()
        |> last()
        |> duplicate(as: "_time", column: "_start")
        |> window(every: inf)
    
    from(bucket: "energy")
      |> range(start: -10d)
      |> filter(fn: (r) => r["_measurement"] == "energy_consumption")
      |> filter(fn: (r) => r["_field"] == "total" or r["_field"] == "2250-M1" or r["_field"] == "2070-M1" or r["_field"] == "2040-M1" or r["_field"] == "1120-M1" or r["_field"] == "107-M1" or r["_field"] == "103-M1" or r["_field"] == "1020-M1")
      |> increase()
      |> last()
      |> yield()
    """

    client = InfluxDBClient(url=cfg['influxdb']['url'], token=cfg['influxdb']['token'], org=cfg['influxdb']['org'])
    df = client.query_api().query_data_frame(query)

    df = df.drop(columns=['result', 'table', '_measurement', 'host', ])
    df['_value'] = pd.to_numeric(df['_value'])


    # Excel
    df_excel = df

    df_excel['_time'] = df_excel['_time'].dt.tz_localize(None)
    df_excel['_start'] = df_excel['_start'].dt.tz_convert(cfg['timezone'])
    df_excel['_start'] = df_excel['_start'].dt.tz_localize(None)
    df_excel['_stop'] = df_excel['_stop'].dt.tz_convert(cfg['timezone'])
    df_excel['_stop'] = df_excel['_stop'].dt.tz_localize(None)

    writer = pd.ExcelWriter(output_file_name + '.xlsx',
                            engine='xlsxwriter',
                            datetime_format='mmm d yyyy hh:mm:ss',
                            date_format='mmmm dd yyyy')

    df_excel.to_excel(writer,
                      sheet_name='Sheet1',
                      columns=['_field', '_value'],
                      header=['Нагрузка', 'Потребление'],
                      index=False,
                      startrow=4)

    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    worksheet.write(0, 0, NAME_FOR_USER)
    worksheet.write(1, 0, 'от')
    worksheet.write(1, 1, f"{df_excel.iloc[0, df_excel.columns.get_loc('_start')]:%Y-%m-%d %H:%M}")
    worksheet.write(2, 0, 'до')
    worksheet.write(2, 1, f"{df_excel.iloc[0, df_excel.columns.get_loc('_stop')]:%Y-%m-%d %H:%M}")

    writer.save()


if __name__ == '__main__':
    report_test()
