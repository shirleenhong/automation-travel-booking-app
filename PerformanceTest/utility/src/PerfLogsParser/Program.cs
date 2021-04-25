using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Configuration;
using System.IO;
using OfficeOpenXml;
using OfficeOpenXml.Drawing.Chart;
using OfficeOpenXml.Style.XmlAccess;
using OfficeOpenXml.Style;
using System.Drawing;
using System.Text.RegularExpressions;
using NLog;

namespace PerfLogsParser
{
    class Program
    {
        private static string PERFLOG_PATH = ConfigurationSettings.AppSettings["PerfLogPath"];
        private static string SEARCH_PATTERN = ConfigurationSettings.AppSettings["SearchPattern"];
        private static string SAVE_PATH = ConfigurationSettings.AppSettings["SavePath"];
        private static string SUMMARY_SAVE_PATH = ConfigurationSettings.AppSettings["SummarySavePath"];
        private static string SAVE_FILENAME = ConfigurationSettings.AppSettings["SaveFileName"];
        private static string SUMMARY_SAVE_FILENAME = ConfigurationSettings.AppSettings["SummarySaveFileName"];
        private static string RETRIEVE_MODE = ConfigurationSettings.AppSettings["RetrieveMode"];
        private static string USER_NAME = ConfigurationSettings.AppSettings["UserName"];
        private static string PASSWORD = ConfigurationSettings.AppSettings["Password"];
        private static string DOMAIN = ConfigurationSettings.AppSettings["Domain"];
        private static string SOURCE_DIRECTORIES = ConfigurationSettings.AppSettings["SourceDirectories"];
        private static string RESPONSE_VARIANCE_CHART = ConfigurationSettings.AppSettings["ResponseTimeAndVarianceChart"];
        private static string MIN_MAX_AVG_CHART = ConfigurationSettings.AppSettings["MinMaxAvgChart"];
        private static string RESP_VAR_FILENAME = ConfigurationSettings.AppSettings["ResponseAndVarianceFileName"];
        private static string MIN_MAX_AVG_FILENAME = ConfigurationSettings.AppSettings["MinMaxAvgFileName"];
        private static string USR_DURATION_FILENAME = ConfigurationSettings.AppSettings["UserDurationPerRun"];
        private static string HTML_GRAPH = ConfigurationSettings.AppSettings["HtmlGraph"];
        private static string DURATION_PAIR_FROM = ConfigurationSettings.AppSettings["DurationPairFrom"];
        private static string DURATION_PAIR_TO = ConfigurationSettings.AppSettings["DurationPairTo"];
        private static string DELETE_LOCAL_LOGS_BEFORE_RUN = ConfigurationSettings.AppSettings["DeleteLocalSyExLogsSetup"];
        private static string DELETE_LOCAL_LOGS_AFTER_RUN = ConfigurationSettings.AppSettings["DeleteLocalSyExLogsTearDown"];
        private static string SKIP_CONNECT_TO_NETWORK = ConfigurationSettings.AppSettings["SkipConnectToNetwork"];
        private static string LOCAL_SOURCE_SYEX_LOGS = ConfigurationSettings.AppSettings["SourceSyExInLocal"];

        private const string RespVarDataFromCsv = "respvardatafromcsv";
        private const string MinMaxAvgDataFromCsv = "minvmaxavgdatafromcsv";
        private const string UserDurationDataFromCsv = "userdurationdatafromcsv";
        private const string FinalHtmlFileName = "PerfGraph.html";
        private const string UserDownloadFolderPath = "userdownloadfolderpath";

        private static Logger logger = LogManager.GetCurrentClassLogger();
        static void Main(string[] args)
        {
            try
            {
                SUMMARY_SAVE_PATH = String.Format(SUMMARY_SAVE_PATH, DateTime.Now.ToString("yyyyMMdd-hhmmss"));                
                CheckIfDirectoryExist(SAVE_PATH);
                CheckIfDirectoryExist(SUMMARY_SAVE_PATH);

                if (Directory.Exists(PERFLOG_PATH))
                {
                    if (Directory.GetFiles(PERFLOG_PATH).Length > 0)
                    {
                        if (bool.Parse(DELETE_LOCAL_LOGS_BEFORE_RUN))
                        {
                            logger.Info(String.Format("Deleting {0} and all its contents...", PERFLOG_PATH));
                            Directory.Delete(PERFLOG_PATH, true);
                        }
                    }                   
                }
                CheckIfDirectoryExist(PERFLOG_PATH);

                string searchPattern = RETRIEVE_MODE == "Today" ? DateTime.Now.ToString("yyyyMMdd") : String.Empty;

                if (bool.Parse(SKIP_CONNECT_TO_NETWORK))
                {
                    logger.Info(String.Format("Getting files from {0}", LOCAL_SOURCE_SYEX_LOGS));
                    foreach (var srcFile in Directory.GetFiles(LOCAL_SOURCE_SYEX_LOGS, String.Format(SEARCH_PATTERN, searchPattern)))
                    {
                        var srcFileInfo = new FileInfo(srcFile);
                        var srcFileNoExt = Path.GetFileNameWithoutExtension(srcFile);
                        var countFilesInDest = Directory.GetFiles(PERFLOG_PATH, String.Format("*{0}*", srcFileNoExt)).Length;
                        string destFileName = countFilesInDest > 0 ? String.Format("{0} ({1}).log", srcFileNoExt, countFilesInDest + 1) : srcFileInfo.Name;
                        logger.Info("Copying {0} to {1}", srcFile, PERFLOG_PATH);
                        File.Copy(srcFile, Path.Combine(PERFLOG_PATH, destFileName));
                    }
                }
                else
                {
                    var credential = new System.Net.NetworkCredential(USER_NAME, PASSWORD, DOMAIN);                    

                    var srcDirectories = SOURCE_DIRECTORIES.Split(';').ToList();

                    foreach (string directory in srcDirectories)
                    {
                        logger.Info(String.Format("Connecting to {0}", directory));

                        using (new ConnectToSharedFolder(directory, credential))
                        {
                            foreach (var srcFile in Directory.GetFiles(directory, String.Format(SEARCH_PATTERN, searchPattern)))
                            {
                                var srcFileInfo = new FileInfo(srcFile);
                                var srcFileNoExt = Path.GetFileNameWithoutExtension(srcFile);
                                var countFilesInDest = Directory.GetFiles(PERFLOG_PATH, String.Format("*{0}*", srcFileNoExt)).Length;
                                string destFileName = countFilesInDest > 0 ? String.Format("{0} ({1}).log", srcFileNoExt, countFilesInDest + 1) : srcFileInfo.Name;
                                logger.Info("Copying {0} to {1}", srcFile, PERFLOG_PATH);
                                File.Copy(srcFile, Path.Combine(PERFLOG_PATH, destFileName));
                            }
                        }
                    }
                }
                

                var dirInfo = new DirectoryInfo(PERFLOG_PATH);

                var files = dirInfo.GetFiles(String.Format(SEARCH_PATTERN, searchPattern)).OrderByDescending(f => f.LastWriteTime).ToList();

                var perfLogEntries = new List<PerfLogEntry>();
                var tempPerfLogEntries = new List<PerfLogEntry>();
                var userTransactionTimes = new List<UserTransactionTime>();
                var durationPairNames = new List<string> { DURATION_PAIR_FROM, DURATION_PAIR_TO };
                var settings = new XmlReaderSettings();
                settings.ConformanceLevel = ConformanceLevel.Fragment;

                foreach (var fileInfo in files)
                {
                    var logDate = new DateTime();
                    string userName = String.Empty;
                    string transactionDate = String.Empty;
                    bool firstLineRead = false;
                    var userTransactionTime = new UserTransactionTime();
                    userTransactionTime.ReadToDate = false;

                    using (var reader = XmlReader.Create(fileInfo.FullName, settings))
                    {
                        logger.Info("Reading {0}", fileInfo.FullName);

                        while (reader.Read())
                        {
                            string className = reader["ClassName"];
                            if (!String.IsNullOrEmpty(className))
                            {
                                logDate = DateTime.Parse(reader["DateTime"]);
                                string methodName = reader["MethodName"];
                                int performance = Int32.Parse(reader["Performance"]);
                                userName = reader["User"];
                                userTransactionTime.UserName = userName;
                                userTransactionTime.TransactionDate = logDate.ToString("yyyyMMdd");

                                if (durationPairNames.Contains(methodName))
                                {
                                    if (methodName == DURATION_PAIR_FROM && !userTransactionTime.ReadToDate)
                                    {
                                        userTransactionTime.FromDate = logDate;
                                    }

                                    if (methodName == DURATION_PAIR_TO && userTransactionTime.ReadToDate)
                                    {
                                        userTransactionTime.ToDate = logDate;
                                    }
                                }

                                var perfLogEntry = perfLogEntries.FirstOrDefault(x => x.GetFormattedDate() == logDate.ToString("yyyyMMdd") &&
                                    x.UserName == userName && x.ClassName == className && x.MethodName == methodName);
                                if (perfLogEntry != null)
                                {
                                    if (performance > perfLogEntry.Max)
                                    {
                                        perfLogEntry.Max = performance;
                                        perfLogEntry.Min = perfLogEntry.Min == 0 ? performance : perfLogEntry.Min;
                                    }
                                    else
                                    {
                                        if (performance < perfLogEntry.Min || perfLogEntry.Min == 0)
                                        {
                                            perfLogEntry.Min = performance;
                                        }
                                    }
                                    perfLogEntry.Count++;
                                    perfLogEntry.Total += performance;
                                }
                                else
                                {
                                    perfLogEntries.Add(new PerfLogEntry
                                    {
                                        LogDate = logDate,
                                        ClassName = className,
                                        MethodName = methodName,
                                        Count = 1,
                                        Min = performance,
                                        Max = performance,
                                        Total = performance,
                                        UserName = userName
                                    });
                                }
                            }
                        }
                        reader.Close();
                        userTransactionTimes.Add(userTransactionTime);
                    }
                }

                #region Create Total

                var totalPerfLogEntries = new List<PerfLogEntry>();

                logger.Info("Creating Total");

                perfLogEntries.ForEach(perfEntry =>
                {
                    var totalPerfLogEntry = totalPerfLogEntries.FirstOrDefault(t => t.GetFormattedDate() == perfEntry.GetFormattedDate()
                            && t.ClassName == perfEntry.ClassName && t.MethodName == perfEntry.MethodName && t.UserName == "Total");

                    if (totalPerfLogEntry == null)
                    {
                        totalPerfLogEntries.Add(new PerfLogEntry
                        {
                            LogDate = perfEntry.LogDate,
                            ClassName = perfEntry.ClassName,
                            MethodName = perfEntry.MethodName,
                            Count = perfEntry.Count,
                            Min = perfEntry.Min,
                            Max = perfEntry.Max,
                            Total = perfEntry.Total,
                            UserName = "Total"
                        });
                    }
                    else
                    {
                        totalPerfLogEntry.Max = totalPerfLogEntry.Max < perfEntry.Max ? perfEntry.Max : totalPerfLogEntry.Max;
                        totalPerfLogEntry.Min = totalPerfLogEntry.Min > perfEntry.Min ? perfEntry.Min : totalPerfLogEntry.Min;
                        totalPerfLogEntry.Total += perfEntry.Total;
                        totalPerfLogEntry.Count += perfEntry.Count;
                    }
                });

                perfLogEntries.AddRange(totalPerfLogEntries);

                #endregion

                #region Create Excel Files
                foreach (string date in perfLogEntries.Select(x => x.GetFormattedDate()).Distinct())
                {
                    int runNumber = 1;
                    while (File.Exists(Path.Combine(SAVE_PATH, String.Format(SAVE_FILENAME, date, runNumber.ToString("00")))))
                    {
                        runNumber++;
                    }

                    var excelFileInfo = new FileInfo(Path.Combine(SAVE_PATH, String.Format(SAVE_FILENAME, date, runNumber.ToString("00"))));

                    logger.Info(String.Format("Creating {0}...", excelFileInfo.FullName));

                    using (ExcelPackage package = new ExcelPackage(excelFileInfo))
                    {
                        var durationSheet = package.Workbook.Worksheets.Add("tempDurationWorksheet");
                        CreateHeaders(durationSheet, null, new List<string> { "User", "Duration(millseconds)", "Average", "TransactionCount" });
                        var re = new Regex(@"\d+$");
                        foreach (var userName in perfLogEntries.Where(d => d.GetFormattedDate() == date).Select(x => x.UserName).Distinct().OrderBy(x =>
                            {
                                int? parsed = null;
                                int temp;
                                bool matchParsed = int.TryParse(re.Match(x).Value, out temp);
                                if (matchParsed) { parsed = temp; }
                                return parsed;
                            }))
                        {
                            var sheet = package.Workbook.Worksheets.Add(userName);

                            CreateHeaders(sheet, new List<string> { "LogDate" });
                            sheet.View.FreezePanes(2, 1); //Freeze Top Row
                            var uniqueClassNames = perfLogEntries.Where(x => x.GetFormattedDate() == date && x.UserName == userName).Select(c => c.ClassName).Distinct();
                            int topRow = 2;
                            int bottomRow;
                            foreach (string className in uniqueClassNames.OrderBy(m => m))
                            {
                                sheet.Cells[String.Format("A{0}", topRow)].LoadFromCollection(
                                    perfLogEntries.Where(x => x.GetFormattedDate() == date && x.ClassName == className && x.UserName == userName)
                                    .OrderBy(m => m.MethodName)
                                    .Select(p => new { p.ClassName, p.MethodName, p.Count, p.Min, p.Avg, p.Max, p.Total, p.UserName }));

                                bottomRow = perfLogEntries.Count(x => x.GetFormattedDate() == date && x.ClassName == className && x.UserName == userName) + topRow;

                                sheet.Cells[String.Format("A{0}:G{0}", bottomRow)].Style.Font.Bold = true;
                                sheet.Cells[String.Format("A{0}:G{0}", bottomRow)].Style.Border.BorderAround(ExcelBorderStyle.Thin);

                                sheet.Column(7).Hidden = true;
                                sheet.Column(8).Hidden = true;

                                sheet.Cells[String.Format("{0}{1}", Columns.DetailedClassName, bottomRow)].Value = String.Format("{0} Total", className);
                                sheet.Cells[String.Format("{0}{1}", Columns.DetailedCount, bottomRow)].Formula = String.Format("SUM({0}{1}:{0}{2})", Columns.DetailedCount, topRow, bottomRow - 1);
                                sheet.Cells[String.Format("{0}{1}", Columns.DetailedMin, bottomRow)].Formula = String.Format("MIN({0}{1}:{0}{2})", Columns.DetailedMin, topRow, bottomRow - 1);
                                sheet.Cells[String.Format("{0}{1}", Columns.DetailedAvg, bottomRow)].Formula = String.Format("{0}{2}/{1}{2}", Columns.DetailedTotal, Columns.DetailedCount, bottomRow);
                                sheet.Cells[String.Format("{0}{1}", Columns.DetailedAvg, bottomRow)].Style.Numberformat.Format = "0";
                                sheet.Cells[String.Format("{0}{1}", Columns.DetailedMax, bottomRow)].Formula = String.Format("MAX({0}{1}:{0}{2})", Columns.DetailedMax, topRow, bottomRow - 1);
                                sheet.Cells[String.Format("{0}{1}", Columns.DetailedTotal, bottomRow)].Formula = String.Format("SUM({0}{1}:{0}{2})", Columns.DetailedTotal, topRow, bottomRow - 1);

                                topRow = bottomRow + 1;
                            }

                            if (userName != "Total")
                            {
                                CreateHeaders(sheet, null, new List<string> { "StartTime", "EndTime", "Duration(Millseconds)" }, false, 10);
                                var userTransactionTime = userTransactionTimes.FirstOrDefault(x => x.UserName == userName && x.TransactionDate == date);

                                if (userTransactionTime.DurationPairs.Count > 0)
                                {
                                    foreach (var durationPair in userTransactionTime.DurationPairs)
                                    {
                                        int endRow = ExcelHelper.GetEndRow(sheet, 10) + 1;
                                        sheet.Cells[String.Format("{0}{1}", Columns.DetailedStartTime, endRow)].Value = durationPair.Item1;
                                        sheet.Cells[String.Format("{0}{1}", Columns.DetailedStartTime, endRow)].Style.Numberformat.Format = "mm/dd/yyyy hh:mm:ss";
                                        sheet.Cells[String.Format("{0}{1}", Columns.DetailedEndTime, endRow)].Value = durationPair.Item2;
                                        sheet.Cells[String.Format("{0}{1}", Columns.DetailedEndTime, endRow)].Style.Numberformat.Format = "mm/dd/yyyy hh:mm:ss";
                                        sheet.Cells[String.Format("{0}{1}", Columns.DetailedDuration, endRow)].Formula = String.Format("ROUND(({0}{2}-{1}{2})*86400000,0)", Columns.DetailedEndTime, Columns.DetailedStartTime, endRow);
                                    }

                                    int sheetDurationRow = ExcelHelper.GetEndRow(sheet, 12);
                                    sheet.Cells[String.Format("{0}{1}", Columns.DetailedDuration, sheetDurationRow + 1)].Formula = String.Format("SUM({0}2:{0}{1})", Columns.DetailedDuration, sheetDurationRow);
                                }
                                int durationSheetCurrentRow = durationSheet.Dimension.End.Row + 1;
                                int sheetTotalDurationRow = ExcelHelper.GetEndRow(sheet, 12);

                                durationSheet.Cells[String.Format("{0}{1}", Columns.DurationUserName, durationSheetCurrentRow)].Value = userName;
                                durationSheet.Cells[String.Format("{0}{1}", Columns.DurationMilliseconds, durationSheetCurrentRow)].Value = userTransactionTime.DurationPairs.Count > 0 ?
                                    ExcelHelper.CalculateValue(sheet.Cells[String.Format("{0}{1}", Columns.DetailedDuration, sheetTotalDurationRow)]) :
                                    0;
                                durationSheet.Cells[String.Format("{0}{1}", Columns.DurationAverage, durationSheetCurrentRow)].Formula = String.Format("{0}{1}/{2}{1}", Columns.DurationMilliseconds, durationSheetCurrentRow, Columns.DurationCount);
                                durationSheet.Cells[String.Format("{0}{1}", Columns.DurationCount, durationSheetCurrentRow)].Value = userTransactionTime.DurationPairs.Count;
                                //sheet.Cells[String.Format("{0}2:{1}2", Columns.DetailedStartTime, Columns.DetailedDuration)].Copy(durationSheet.Cells[String.Format("B{0}", durationSheetEndRow + 1)]);
                            }
                        }
                        //durationSheet.Cells[durationSheet.Dimension.End.Row + 1, 4].Formula = String.Format("SUM(D2:D{0})", durationSheet.Dimension.End.Row);
                        durationSheet.Cells[String.Format("{0}1:{1}{2}", Columns.DurationUserName, Columns.DurationCount, durationSheet.Dimension.End.Row)].Copy(package.Workbook.Worksheets["Total"].Cells[String.Format("{0}1", Columns.DetailedTotalUser)]);
                        package.Workbook.Worksheets.Delete(durationSheet);
                        package.Workbook.Worksheets.MoveToStart("Total");
                        package.Save();
                    }
                }

                CreateSummary();
                #endregion

                logger.Info("Completed.");
            }
            catch (Exception ex)
            {
                logger.Error("An error has occured.");
                logger.Error(String.Format("Error Details: {0}", ex.Message));
                logger.Error(String.Format("Inner exception: {0}", ex.InnerException));
                logger.Error(String.Format("Stack Trace: {0}", ex.StackTrace));
            }
            finally
            {
                #region Delete logs

                if (bool.Parse(DELETE_LOCAL_LOGS_AFTER_RUN))
                {
                    logger.Info(String.Format("Deleting {0} and all its contents...", PERFLOG_PATH));
                    Directory.Delete(PERFLOG_PATH, true);
                }
                Console.WriteLine("Press any key to continue.......");
                Console.Read();

                #endregion
            }

        }

        static void CheckIfDirectoryExist(string path)
        {
            if (!Directory.Exists(path))
            {
                logger.Info(String.Format("{0} does not exist. Creating it now.", path));
                Directory.CreateDirectory(path);
            }
        }
        static void CreateHeaders(ExcelWorksheet sheet, List<string> exclude = null, List<string> customHeaders = null, bool rowMode = false, int colStart = 1)
        {
            var t = typeof(PerfLogEntry);
            var headers = customHeaders == null ? t.GetProperties().Select(p => p.Name).ToArray() : customHeaders.ToArray();

            if (exclude != null)
                headers = headers.Where(x => !exclude.Contains(x)).ToArray();

            for (int i = 0; i < headers.Count(); i++)
            {
                int row = rowMode ? i + 1 : 1;
                int col = rowMode ? 1 : i + colStart;

                sheet.Cells[row, col].Value = headers[i];
                sheet.Cells[row, col].Style.Font.Bold = true;
                sheet.Cells[row, col].Style.Fill.PatternType = ExcelFillStyle.Solid;
                sheet.Cells[row, col].Style.Fill.BackgroundColor.SetColor(Color.FromArgb(79, 129, 189));
                sheet.Cells[row, col].Style.Font.Color.SetColor(Color.White);
            }
        }

        static void CreateSummary()
        {
            var dirInfo = new DirectoryInfo(SAVE_PATH);
            string summaryFileName = Path.Combine(SUMMARY_SAVE_PATH, String.Format(SUMMARY_SAVE_FILENAME, DateTime.Now.ToString("yyyyMMddhhmmss")));

            logger.Info(String.Format("Creating {0}...", summaryFileName));

            var summaryPackage = new ExcelPackage(new FileInfo(summaryFileName));
            var summarySheet = summaryPackage.Workbook.Worksheets.Add("Summary");
            CreateHeaders(summarySheet,
                null,
                new List<string> { "Date",
                    "Number of Users",
                    "Count",
                    "Min",
                    "Avg",
                    "Max",
                    "Total",
                    "Variance" }, true);

            foreach (var file in dirInfo.GetFiles("PerfLog*Run*.xlsx").OrderBy(f => f.Name))
            {
                logger.Info(String.Format("Transferring {0} to {1}...", file.FullName, summaryFileName));

                using (var package = new ExcelPackage(file))
                {
                    int numOfUsrs = package.Workbook.Worksheets.Count - 1;
                    var totalSheet = package.Workbook.Worksheets["Total"];
                    var totalCells = totalSheet.Cells.Where(cell => cell.Address.Contains("B") && String.IsNullOrEmpty((string)cell.Value));

                    string sheetName = file.Name.Replace("PerfLog_", String.Empty).Replace(".xlsx", String.Empty);

                    var summaryTotalSheet = summaryPackage.Workbook.Worksheets.Add(sheetName);
                    CreateHeaders(summaryTotalSheet, new List<string> { "LogDate", "MethodName", "UserName" });

                    int summaryTotalEndRow = 0;

                    foreach (var cell in totalCells)
                    {
                        int rowNumber = ExcelHelper.GetRowNumber(cell);
                        summaryTotalEndRow = summaryTotalSheet.Dimension.End.Row + 1;

                        summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalClassName, summaryTotalEndRow)].Value = totalSheet.Cells[String.Format("{0}{1}", Columns.DetailedTotalClassName, rowNumber)].Value.ToString().Replace(" Total", String.Empty);
                        summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalCount, summaryTotalEndRow)].Value = ExcelHelper.CalculateValue(totalSheet.Cells[String.Format("{0}{1}", Columns.DetailedTotalCount, rowNumber)]);
                        summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalMin, summaryTotalEndRow)].Value = ExcelHelper.CalculateValue(totalSheet.Cells[String.Format("{0}{1}", Columns.DetailedTotalMin, rowNumber)]);
                        summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalAvg, summaryTotalEndRow)].Value = ExcelHelper.CalculateValue(totalSheet.Cells[String.Format("{0}{1}", Columns.DetailedTotalAvg, rowNumber)]);
                        summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalAvg, summaryTotalEndRow)].Style.Numberformat.Format = "0";
                        summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalMax, summaryTotalEndRow)].Value = ExcelHelper.CalculateValue(totalSheet.Cells[String.Format("{0}{1}", Columns.DetailedTotalMax, rowNumber)]);
                        summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalTotal, summaryTotalEndRow)].Value = ExcelHelper.CalculateValue(totalSheet.Cells[String.Format("{0}{1}", Columns.DetailedTotalTotal, rowNumber)]);
                    }

                    summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalCount, summaryTotalEndRow + 1)].Formula = String.Format("SUM({0}2:{0}{1})", Columns.SummaryTotalCount, summaryTotalEndRow);
                    summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalMin, summaryTotalEndRow + 1)].Formula = String.Format("SUM({0}2:{0}{1})", Columns.SummaryTotalMin, summaryTotalEndRow);
                    summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalAvg, summaryTotalEndRow + 1)].Formula = String.Format("SUM({0}2:{0}{1})", Columns.SummaryTotalAvg, summaryTotalEndRow);
                    summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalMax, summaryTotalEndRow + 1)].Formula = String.Format("SUM({0}2:{0}{1})", Columns.SummaryTotalMax, summaryTotalEndRow);
                    summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalTotal, summaryTotalEndRow + 1)].Formula = String.Format("SUM({0}2:{0}{1})", Columns.SummaryTotalTotal, summaryTotalEndRow);

                    totalSheet.Cells[String.Format("{0}1:{1}{2}", Columns.DetailedTotalUser, Columns.DetailedTotalDurationCount, ExcelHelper.GetEndRow(totalSheet, 13))].Copy(summaryTotalSheet.Cells["H1"]);

                    int endColumn = summarySheet.Dimension.End.Column + 1;
                    summarySheet.Cells[1, endColumn].Value = sheetName;
                    summarySheet.Cells[2, endColumn].Value = package.Workbook.Worksheets.Count - 1;
                    summarySheet.Cells[3, endColumn].Value = ExcelHelper.CalculateValue(summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalCount, summaryTotalEndRow + 1)]);
                    summarySheet.Cells[4, endColumn].Value = ExcelHelper.CalculateValue(summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalMin, summaryTotalEndRow + 1)]);
                    summarySheet.Cells[5, endColumn].Value = ExcelHelper.CalculateValue(summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalAvg, summaryTotalEndRow + 1)]);
                    summarySheet.Cells[6, endColumn].Value = ExcelHelper.CalculateValue(summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalMax, summaryTotalEndRow + 1)]);
                    summarySheet.Cells[7, endColumn].Value = ExcelHelper.CalculateValue(summaryTotalSheet.Cells[String.Format("{0}{1}", Columns.SummaryTotalTotal, summaryTotalEndRow + 1)]);

                    if (endColumn == 2)
                    {
                        summarySheet.Cells[8, endColumn].Value = 0;
                    }
                    else
                    {
                        summarySheet.Cells[8, endColumn].Formula = String.Format("({0}-{1})/{0}", summarySheet.Cells[7, endColumn].Address, summarySheet.Cells[7, endColumn - 1].Address);
                    }
                }
            }
            #region Transfer Users to a separate sheet

            var summaryUsersPerRun = summaryPackage.Workbook.Worksheets.Add("Users");
            CreateHeaders(summaryUsersPerRun, null, new List<string> { "UserName" });

            foreach (var sheet in summaryPackage.Workbook.Worksheets.Where(w => w.Name != "Summary" && w != summaryUsersPerRun))
            {
                int endRow = summaryUsersPerRun.Dimension.End.Row;
                int endColumn = summaryUsersPerRun.Dimension.End.Column;
                summaryUsersPerRun.Cells[1, endColumn + 1].Value = sheet.Name;
                endColumn = summaryUsersPerRun.Dimension.End.Column;
                for (int i = 2; i <= ExcelHelper.GetEndRow(sheet, 8); i++)
                {
                    endRow = summaryUsersPerRun.Dimension.End.Row;

                    ExcelRangeBase cell = summaryUsersPerRun.Cells["A:A"].FirstOrDefault(c => String.Equals(c.Text, sheet.Cells[i, 8].Text, StringComparison.InvariantCulture));

                    if (cell != null)
                    {
                        summaryUsersPerRun.Cells[ExcelHelper.GetRowNumber(cell), endColumn].Value = ExcelHelper.CalculateValue(sheet.Cells[i, 9]);
                    }
                    else
                    {
                        summaryUsersPerRun.Cells[endRow + 1, 1].Value = sheet.Cells[i, 8].Value;
                        summaryUsersPerRun.Cells[endRow + 1, endColumn].Value = ExcelHelper.CalculateValue(sheet.Cells[i, 9]);
                    }
                }
            }

            #endregion

            #region Create CSV Summary

            var csvSheet = summaryPackage.Workbook.Worksheets.Add("CsvSheet");
            var respVarSheet = summaryPackage.Workbook.Worksheets.Add("RespVarSheet");
            var minMaxSheet = summaryPackage.Workbook.Worksheets.Add("minMaxSheet");

            for (int col = 1; col <= summarySheet.Dimension.End.Column; col++)
            {
                for (int row = 1; row <= summarySheet.Dimension.End.Row; row++)
                {
                    csvSheet.Cells[col, row].Value = ExcelHelper.CalculateValue(summarySheet.Cells[row, col]);
                }
            }
            csvSheet.Cells.Copy(respVarSheet.Cells["A1"]);
            respVarSheet.DeleteColumn(2, 5);
            for (int i = 2; i <= ExcelHelper.GetEndRow(respVarSheet, 2); i++)
            {
                respVarSheet.Cells[i, 2].Value = ExcelHelper.ConvertToMinutes(respVarSheet.Cells[i, 2].Value);
                respVarSheet.Cells[i, 3].Value = ExcelHelper.ConvertToPercent(respVarSheet.Cells[i, 3].Value);
            }

            csvSheet.Cells.Copy(minMaxSheet.Cells["A1"]);
            minMaxSheet.DeleteColumn(7, 2);
            minMaxSheet.DeleteColumn(2, 2);

            string respVarFileName = BuildHtmlGraphPath(RESP_VAR_FILENAME);
            string minMaxAvgFileName = BuildHtmlGraphPath(MIN_MAX_AVG_FILENAME);
            string userDurationFileName = BuildHtmlGraphPath(USR_DURATION_FILENAME);

            logger.Info(String.Format("Creating {0}...", respVarFileName));
            EpplusCsvConverter.ConvertToCsv(respVarSheet, respVarFileName);

            logger.Info(String.Format("Creating {0}...", minMaxAvgFileName));
            EpplusCsvConverter.ConvertToCsv(minMaxSheet, minMaxAvgFileName);

            logger.Info(String.Format("Creating {0}...", userDurationFileName));
            EpplusCsvConverter.ConvertToCsv(summaryUsersPerRun, userDurationFileName);

            string htmlPage = File.ReadAllText(HTML_GRAPH);
            string respVarCsv = File.ReadAllText(respVarFileName);
            string minvMaxAvgCsv = File.ReadAllText(minMaxAvgFileName);
            string userDurationCsv = File.ReadAllText(userDurationFileName);
            string downloadFolder = Environment.GetEnvironmentVariable("USERPROFILE") + @"\" + "Downloads" + @"\";
            string finalHtmlPageContent = string.Empty;
            finalHtmlPageContent = htmlPage.Replace(RespVarDataFromCsv, respVarCsv);
            finalHtmlPageContent = finalHtmlPageContent.Replace(MinMaxAvgDataFromCsv, minvMaxAvgCsv);
            finalHtmlPageContent = finalHtmlPageContent.Replace(UserDurationDataFromCsv, userDurationCsv);
            finalHtmlPageContent = finalHtmlPageContent.Replace(UserDownloadFolderPath, downloadFolder.Replace(@"\", "/"));
            File.WriteAllText(Path.Combine(SUMMARY_SAVE_PATH, FinalHtmlFileName), finalHtmlPageContent);

            //var htmlGraphFileInfo = new FileInfo(HTML_GRAPH);
            //File.Copy(htmlGraphFileInfo.FullName, Path.Combine(SUMMARY_SAVE_PATH, htmlGraphFileInfo.Name));

            summaryPackage.Workbook.Worksheets.Delete(csvSheet);
            summaryPackage.Workbook.Worksheets.Delete(respVarSheet);
            summaryPackage.Workbook.Worksheets.Delete(minMaxSheet);

            #endregion

            #region Create Chart

            logger.Info("Creating Response and Variance chart...");
            var respTimeAndVarianceChart = summarySheet.Drawings.AddChart("ResponseTimeAndVariance", eChartType.ColumnClustered);
            var respTimeAndVarianceChartXml = new XmlDocument();
            respTimeAndVarianceChartXml.Load(RESPONSE_VARIANCE_CHART);
            var nsmgr = new XmlNamespaceManager(respTimeAndVarianceChartXml.NameTable);
            nsmgr.AddNamespace("c", "http://schemas.openxmlformats.org/drawingml/2006/chart");

            int endCol = summarySheet.Dimension.End.Column;
            var catRange = summarySheet.Cells[1, 2, 1, endCol];
            var totalRange = summarySheet.Cells[7, 2, 7, endCol];
            var varianceRange = summarySheet.Cells[8, 2, 8, endCol];

            var totalCatElement = (XmlElement)respTimeAndVarianceChartXml.SelectSingleNode(@"/*/c:chart/c:plotArea/c:barChart/c:ser/c:cat/c:strRef/c:f", nsmgr);
            var totalValElement = (XmlElement)respTimeAndVarianceChartXml.SelectSingleNode(@"/*/c:chart/c:plotArea/c:barChart/c:ser/c:val/c:numRef/c:f", nsmgr);
            var varianceCatElement = (XmlElement)respTimeAndVarianceChartXml.SelectSingleNode(@"/*/c:chart/c:plotArea/c:lineChart/c:ser/c:cat/c:strRef/c:f", nsmgr);
            var varianceValElement = (XmlElement)respTimeAndVarianceChartXml.SelectSingleNode(@"/*/c:chart/c:plotArea/c:lineChart/c:ser/c:val/c:numRef/c:f", nsmgr);

            totalCatElement.InnerText = catRange.FullAddressAbsolute;
            varianceCatElement.InnerText = catRange.FullAddressAbsolute;
            totalValElement.InnerText = totalRange.FullAddressAbsolute;
            varianceValElement.InnerText = varianceRange.FullAddressAbsolute;

            respTimeAndVarianceChart.ChartXml.InnerXml = respTimeAndVarianceChartXml.InnerXml;
            respTimeAndVarianceChart.SetPosition(200, 1);
            respTimeAndVarianceChart.SetSize(840, 475);

            logger.Info("Creating Min, Max and Avg chart...");
            var minMaxAvgChart = summarySheet.Drawings.AddChart("MinMaxAvgChart", eChartType.Line);
            var minMaxAvgChartXml = new XmlDocument();
            minMaxAvgChartXml.Load(MIN_MAX_AVG_CHART);
            var nsmgr2 = new XmlNamespaceManager(minMaxAvgChartXml.NameTable);
            nsmgr2.AddNamespace("c", "http://schemas.openxmlformats.org/drawingml/2006/chart");

            var minRange = summarySheet.Cells[4, 2, 4, endCol];
            var maxRange = summarySheet.Cells[6, 2, 6, endCol];
            var avgRange = summarySheet.Cells[5, 2, 5, endCol];

            string xpath = @"/*/c:chart/c:plotArea/c:lineChart/c:ser[c:tx/c:strRef/c:strCache/c:pt/c:v='{0}']/c:{1}/c:{2}/c:f";

            var totalMinCatElement = (XmlElement)minMaxAvgChartXml.SelectSingleNode(String.Format(xpath, "Min", "cat", "strRef"), nsmgr2);
            var totalMinValElement = (XmlElement)minMaxAvgChartXml.SelectSingleNode(String.Format(xpath, "Min", "val", "numRef"), nsmgr2);
            var totalMaxCatElement = (XmlElement)minMaxAvgChartXml.SelectSingleNode(String.Format(xpath, "Max", "cat", "strRef"), nsmgr2);
            var totalMaxValElement = (XmlElement)minMaxAvgChartXml.SelectSingleNode(String.Format(xpath, "Max", "val", "numRef"), nsmgr2);
            var totalAvgCatElement = (XmlElement)minMaxAvgChartXml.SelectSingleNode(String.Format(xpath, "Avg", "cat", "strRef"), nsmgr2);
            var totalAvgValElement = (XmlElement)minMaxAvgChartXml.SelectSingleNode(String.Format(xpath, "Avg", "val", "numRef"), nsmgr2);

            totalMinCatElement.InnerText = catRange.FullAddressAbsolute;
            totalMaxCatElement.InnerText = catRange.FullAddressAbsolute;
            totalAvgCatElement.InnerText = catRange.FullAddressAbsolute;
            totalMinValElement.InnerText = minRange.FullAddressAbsolute;
            totalMaxValElement.InnerText = maxRange.FullAddressAbsolute;
            totalAvgValElement.InnerText = avgRange.FullAddressAbsolute;

            minMaxAvgChart.ChartXml.InnerXml = minMaxAvgChartXml.InnerXml;
            minMaxAvgChart.SetPosition(200, 850);
            minMaxAvgChart.SetSize(840, 475);

            logger.Info("Creating User Duration per Run chart...");
            var userDurationChart = summarySheet.Drawings.AddChart("UserDurationChart", eChartType.Line);

            int usersEndRow = summaryUsersPerRun.Dimension.End.Row;

            ExcelRangeBase users = summaryUsersPerRun.Cells[String.Format("A2:A{0}", usersEndRow)];

            for (int i = 2; i <= summaryUsersPerRun.Dimension.End.Column; i++)
            {
                var serie = userDurationChart.Series.Add(summaryUsersPerRun.Cells[2, i, usersEndRow, i], users);
                serie.HeaderAddress = summaryUsersPerRun.Cells[1, i];
            }
            userDurationChart.Title.Text = "User Duration per Run";
            userDurationChart.SetPosition(680, 1);
            userDurationChart.SetSize(1685, 616);

            #endregion

            summaryPackage.Save();
        }

        static string BuildHtmlGraphPath(string fileName)
        {
            return Path.Combine(SUMMARY_SAVE_PATH, fileName);
        }
    }
}
