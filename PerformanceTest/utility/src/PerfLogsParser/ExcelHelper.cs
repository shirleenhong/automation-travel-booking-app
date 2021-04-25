using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using OfficeOpenXml;
using OfficeOpenXml.Style.XmlAccess;
using OfficeOpenXml.Style;

namespace PerfLogsParser
{
    public class ExcelHelper
    {
        public static int GetRowNumber(ExcelRangeBase cell)
        {            
            string[] addressParsed = cell.FullAddressAbsolute.Split('$');

            return Int32.Parse(addressParsed[addressParsed.Length - 1]);
        }

        public static int GetEndRow(ExcelWorksheet sheet, int column)
        {
            var row = sheet.Dimension.End.Row;
            while (row >= 1)
            {
                var range = sheet.Cells[row, column];
                if (range.Any(c => !string.IsNullOrEmpty(CalculateValue(c).ToString())))
                {
                    break;
                }
                row--;
            }
            return row;
        }

        public static object CalculateValue(ExcelRangeBase cell)
        {
            cell.Calculate();
            return cell.Value;
        }

        public static double ConvertToMinutes(object milliseconds)
        {
            return TimeSpan.FromMilliseconds(Convert.ToDouble(milliseconds)).TotalMinutes;
        }

        public static double ConvertToPercent(object val)
        {
            return Convert.ToDouble(val) * 100;
        }
    }

    public class Columns
    {
        //Detailed
        public static string DetailedClassName = "A";
        public static string DetailedMethodName = "B";
        public static string DetailedCount = "C";
        public static string DetailedMin = "D";
        public static string DetailedAvg = "E";
        public static string DetailedMax = "F";
        public static string DetailedTotal = "G";
        public static string DetailedUserName = "H";
        public static string DetailedStartTime = "J";
        public static string DetailedEndTime = "K";
        public static string DetailedDuration = "L";
        //Detailed-Total
        public static string DetailedTotalClassName = "A";
        public static string DetailedTotalMethodName = "B";
        public static string DetailedTotalCount = "C";
        public static string DetailedTotalMin = "D";
        public static string DetailedTotalAvg = "E";
        public static string DetailedTotalMax = "F";
        public static string DetailedTotalTotal = "G";
        public static string DetailedTotalUserName = "H";
        public static string DetailedTotalUser = "J";
        public static string DetailedTotalDuration = "K";
        public static string DetailedTotalDurationCount = "M";
        //Detailed-tempDurationWorksheet
        public static string DurationUserName = "A";
        public static string DurationMilliseconds = "B";
        public static string DurationAverage = "C";
        public static string DurationCount = "D";
        //Summary

        //Summary-Total
        public static string SummaryTotalClassName = "A";
        public static string SummaryTotalCount = "B";
        public static string SummaryTotalMin = "C";
        public static string SummaryTotalAvg = "D";
        public static string SummaryTotalMax = "E";
        public static string SummaryTotalTotal = "F";
        public static string SummaryTotalUser = "H";
        public static string SummaryTotalDuration = "I";
    }
}
