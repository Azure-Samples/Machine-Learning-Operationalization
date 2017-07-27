
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleApp1
{
    class Program
    {
        // Web Service URL (you can do $az ml service view realtime -n myservicename to get the post url)
        private const string URL = "http://<yourseviceipaddress>:8001/api/v1/service/skdigitsapp/score";

        // Web service input data
        private const string DATA = @"[[0.0,0.0,10.0,14.0,8.0,1.0,0.0,0.0,0.0,2.0,16.0,14.0,6.0,1.0,0.0,0.0,0.0,0.0,15.0,15.0,8.0,15.0,0.0,0.0,0.0,0.0,5.0,16.0,16.0,10.0,0.0,0.0,0.0,0.0,12.0,15.0,15.0,12.0,0.0,0.0,0.0,4.0,16.0,6.0,4.0,16.0,6.0,0.0,0.0,8.0,16.0,10.0,8.0,16.0,8.0,0.0,0.0,1.0,8.0,12.0,14.0,12.0,1.0,0.0]";

        static void Main(string[] args)
        {
            Program.PostRequest();
        }

        private static void PostRequest()
        {
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(URL);
            request.Method = "POST";
            request.ContentType = "application/json";
            request.ContentLength = DATA.Length;
            using (Stream webStream = request.GetRequestStream())
            using (StreamWriter requestWriter = new StreamWriter(webStream, System.Text.Encoding.ASCII))
            {
                requestWriter.Write(DATA);
            }

            try
            {
                WebResponse webResponse = request.GetResponse();
                using (Stream webStream = webResponse.GetResponseStream())
                {
                    if (webStream != null)
                    {
                        using (StreamReader responseReader = new StreamReader(webStream))
                        {
                            string response = responseReader.ReadToEnd();
                            Console.Out.WriteLine(response);
                            Console.ReadLine();
                        }
                    }
                }
            }
            catch (Exception e)
            {
                Console.Out.WriteLine("-----------------");
                Console.Out.WriteLine(e.Message);
                Console.ReadLine();
            }
        }
    }
}
