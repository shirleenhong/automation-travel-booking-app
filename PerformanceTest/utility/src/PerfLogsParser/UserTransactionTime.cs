using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace PerfLogsParser
{
    public class UserTransactionTime
    {
        public string UserName { get; set; }
        public string TransactionDate { get; set; }
        public DateTime FromDate 
        {
            get { return _fromDate; }
            set 
            {
                _fromDate = value;
                this.ReadToDate = true;
            }
        }
        public DateTime ToDate 
        {
            get { return _toDate; }
            set
            {
                _toDate = value;
                AddDurationPair();
                this.ReadToDate = false;
            }
        }

        public bool ReadToDate { get; set; }
        public List<Tuple<DateTime, DateTime>> DurationPairs { get; set; }

        private DateTime _fromDate;
        private DateTime _toDate;
        public UserTransactionTime()
        {
            DurationPairs = new List<Tuple<DateTime, DateTime>>();
            _fromDate = new DateTime();
            _toDate = new DateTime();
        }

        public void AddDurationPair()
        {
            DurationPairs.Add(new Tuple<DateTime, DateTime>(FromDate, _toDate));
        }
    }
}
