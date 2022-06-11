using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using Outlook = Microsoft.Office.Interop.Outlook;
using System.Windows.Forms;
using Office = Microsoft.Office.Core;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using System.Web.Script.Serialization;
using Newtonsoft.Json;

namespace SmartFilterAddin
{
    public class Email
    {
        public string Body { get; set; }
        public string Subject { get; set; }

        public Email(string subject ,string body)
        {
            this.Subject = subject;
            this.Body = body;
        }
    }

    public class ResultObj
    {
        public string Result { get; set; }
    }

    public class TrainSample
    {
        public string Subject;
        public string Body;
        public int Output;
        public string FilterName;

        public TrainSample(Email mail,int val,string filter)
        {
            this.Subject = mail.Subject;
            this.Body = mail.Body;
            this.Output = val;
            this.FilterName = filter;
        }
    }

    public class Filter_Result
    {
        public Dictionary<string, int> Result;
    }

    public class Filter_Json
    {
        public List<string> Result { get; set; }
    }


    public partial class ThisAddIn
    {
        private Outlook.NameSpace outlookNamespace;
        private Outlook.MAPIFolder inbox;
        private Outlook.Items items;

        public static HttpClient client = null;

        public static List<string> listOfFilters = new List<string>();

        private static string ServerName = "localhost";

        private void ThisAddIn_Startup(object sender, System.EventArgs e)
        {
            outlookNamespace = this.Application.GetNamespace("MAPI");

            // Get inbox folder. 
            inbox = outlookNamespace.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderInbox);

            // items represents collection of mails in inbox, add event handler. 
            items = inbox.Items;
            items.ItemAdd += new Outlook.ItemsEvents_ItemAddEventHandler(InboxFolderItemAddAsync);
            client = new HttpClient();

            client.BaseAddress = new Uri(string.Format("http://{0}:5000", ServerName));
            client.DefaultRequestHeaders.Accept.Clear();

            this.Populate_Filters();
        }

        private async void Populate_Filters()
        {
            try
            {
                await Task.Run(async () =>
                {
                    HttpResponseMessage response = await client.GetAsync(
                        "listFilters");
                    string responseString = await response.Content.ReadAsStringAsync();
                    JavaScriptSerializer oJS = new JavaScriptSerializer();
                    Filter_Json filter_json = new Filter_Json();
                    filter_json = oJS.Deserialize<Filter_Json>(responseString);

                    foreach (string s in filter_json.Result)
                    {
                        ThisAddIn.listOfFilters.Add(s);
                    }
                });
            }
            catch(Exception exp)
            {
                Console.Write(exp.Message);
            }
            
        }

        /// <summary>
        /// This method is called when a new object(mail) is added to inbox folder. 
        /// </summary>
        /// <param name="Item">Mail item</param>
        async void InboxFolderItemAddAsync(object Item)
        {
            try
            {
                // Create a new product
                Outlook.MailItem mailItem = (Outlook.MailItem)Item;
                Email myEmail = new Email(mailItem.Subject, mailItem.Body);

                var myContent = JsonConvert.SerializeObject(myEmail);

                HttpContent byteContent = new StringContent(myContent, Encoding.UTF8, "application/json");
                byteContent.Headers.ContentType = new MediaTypeHeaderValue("application/json");


                await Task.Run(async () =>
                {
                    HttpResponseMessage response = await client.PostAsync(
                     "predict", byteContent);
                    string responseString = await response.Content.ReadAsStringAsync();
                    JavaScriptSerializer oJS = new JavaScriptSerializer();
                    Filter_Result obj = new Filter_Result();
                    obj = oJS.Deserialize<Filter_Result>(responseString);
                    string tag = "";
                    bool comma_flag = false;
                    foreach(string key in obj.Result.Keys)
                    {              
                        if (obj.Result[key] == 1)
                        {
                            if (comma_flag)
                                tag += ", ";
                            tag += key;
                            comma_flag = true;
                        }
                    }
                    if (tag == "")
                    {
                        tag = "Misc Category";
                        mailItem.Categories += tag;
                    }
                    else
                    {
                        tag += " Category";
                        mailItem.Categories += tag;
                        MessageBox.Show("Received mail falling under " + tag + "\n\n " + mailItem.Subject + " \n\n\n" + mailItem.Body);
                    }
                                    
                });

            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }

        private void ThisAddIn_Shutdown(object sender, System.EventArgs e)
        {
            // Note: Outlook no longer raises this event. If you have code that 
            //    must run when Outlook shuts down, see https://go.microsoft.com/fwlink/?LinkId=506785
        }

        #region VSTO generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InternalStartup()
        {
            this.Startup += new System.EventHandler(ThisAddIn_Startup);
            this.Shutdown += new System.EventHandler(ThisAddIn_Shutdown);
        }
        
        #endregion
    }
}
