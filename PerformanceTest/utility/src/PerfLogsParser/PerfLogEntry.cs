using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PerfLogsParser
{
    public class PerfLogEntry
    {
        public DateTime LogDate { get; set; }
        public string ClassName { get; set; }
        public string MethodName { get; set; }
        public int Count { get; set; }
        public int Min { get; set; }
        public double Avg
        {
            get
            {
                return Total == 0 || Count == 0 
                    ? 0 
                    : Math.Round((double)Total / (double)Count, MidpointRounding.AwayFromZero);
            }
        }
        public int Max { get; set; }

        public int Total { get; set; }

        public string UserName { get; set; }

        public string GetFormattedDate()
        {
            return LogDate.ToString("yyyyMMdd");
        }
    }
}
