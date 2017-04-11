using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.IO;

namespace CameraAppDemo
{
    public static class FetchAsync
    {
        public static async Task<string> CallWebService(string verb, string url, string requestBody = "")
        {
            string jsonDoc = "";
            // Create an HTTP web request using the URL:
            HttpWebRequest request = (HttpWebRequest)HttpWebRequest.Create(new Uri(url));

            request.Method = verb;
            if (requestBody != "")
            {
                request.ContentType = "application/json";
                ASCIIEncoding encoding = new ASCIIEncoding();

                byte[] data = encoding.GetBytes(requestBody);
                request.ContentLength = data.Length;
                Stream myReqStream = null;
                try
                {
                    myReqStream = request.GetRequestStream();
                    myReqStream.Write(data, 0, data.Length);
                    myReqStream.Close();
                }
                catch (Exception e)
                {
                    Console.Write(e.Message);
                }
            }

            try
            {
                using (WebResponse response = await request.GetResponseAsync())
                {
                    if (response.ContentLength > 0)
                    {
                        // Get a stream representation of the HTTP web response:
                        using (Stream stream = response.GetResponseStream())
                        {
                            // Use this stream to build a JSON document object:
                            jsonDoc = await Task.Run(() =>
                            {
                                byte[] bytes = new byte[response.ContentLength + 10];
                                int numBytesToRead = (int)response.ContentLength;
                                int numBytesRead = 0;
                                do
                                {
                                    // Read may return anything from 0 to 10.
                                    int n = stream.Read(bytes, numBytesRead, 10);
                                    numBytesRead += n;
                                    numBytesToRead -= n;
                                } while (numBytesToRead > 0);
                                return System.Text.Encoding.Default.GetString(bytes);
                            });
                        }
                    }
                }
            }
            catch (WebException e)
            {
                Console.Write(e.Message);
            }
            return jsonDoc;
        }
    }
}
