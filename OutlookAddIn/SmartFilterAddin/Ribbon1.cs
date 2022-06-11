using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.Office.Tools.Ribbon;
using Outlook = Microsoft.Office.Interop.Outlook;
using System.Windows.Forms;
using Newtonsoft.Json;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using System.Web.Script.Serialization;

namespace SmartFilterAddin
{
    public partial class Ribbon1
    {
        private int selectedFilter;

        private void Ribbon1_Load(object sender, RibbonUIEventArgs e)
        {
           foreach(string s in ThisAddIn.listOfFilters)
            {
                RibbonDropDownItem item = this.Factory.CreateRibbonDropDownItem();
                item.Label = s;
                this.dropDown1.Items.Add(item);
            }
            selectedFilter = 0;
        }

        private void dropDown1_SelectionChanged(object sender, RibbonControlEventArgs e)
        {
            MessageBox.Show("Selected filter to train changed to " + dropDown1.SelectedItem.Label);
            selectedFilter = dropDown1.SelectedItemIndex;
        }

        private void button1_Click(object sender, RibbonControlEventArgs e)
        {
            Form1 form = new Form1();
            form.Show();
        }

        async private void button2_Click(object sender, RibbonControlEventArgs e)
        {
            try
            {
                if (Globals.ThisAddIn.Application.ActiveExplorer().Selection.Count > 0)
                {
                    Object selObject = Globals.ThisAddIn.Application.ActiveExplorer().Selection[1];
                    if (selObject is Outlook.MailItem)
                    {
                        // Create a new product
                        Outlook.MailItem mailItem = (Outlook.MailItem)selObject;
                        Email myEmail = new Email(mailItem.Subject, mailItem.Body);

                        TrainSample sample = new TrainSample(myEmail, 1, this.dropDown1.SelectedItem.Label);

                        var myContent = JsonConvert.SerializeObject(sample);

                        HttpContent byteContent = new StringContent(myContent, Encoding.UTF8, "application/json");
                        byteContent.Headers.ContentType = new MediaTypeHeaderValue("application/json");

                        await Task.Run(async () =>
                        {
                            HttpResponseMessage response = await ThisAddIn.client.PostAsync(
                                "train", byteContent);
                            string responseString = await response.Content.ReadAsStringAsync();
                            JavaScriptSerializer oJS = new JavaScriptSerializer();
                            ResultObj obj = new ResultObj();
                            obj = oJS.Deserialize<ResultObj>(responseString);
                            int flag = int.Parse(obj.Result);
                            if (flag == 1)
                            {
                                MessageBox.Show("Successfully added as positive example to Filter");
                            }
                            else
                            {
                                MessageBox.Show("Some error occured");
                            }
                        });
                    }
                }
            }
            catch (Exception exp)
            {
                Console.WriteLine(exp.Message);
            }
        }

        async private void button3_Click(object sender, RibbonControlEventArgs e)
        {
            try
            {
                if (Globals.ThisAddIn.Application.ActiveExplorer().Selection.Count > 0)
                {
                    Object selObject = Globals.ThisAddIn.Application.ActiveExplorer().Selection[1];
                    if (selObject is Outlook.MailItem)
                    {
                        // Create a new product
                        Outlook.MailItem mailItem = (Outlook.MailItem)selObject;
                        Email myEmail = new Email(mailItem.Subject, mailItem.Body);

                        TrainSample sample = new TrainSample(myEmail, 0, this.dropDown1.SelectedItem.Label);

                        var myContent = JsonConvert.SerializeObject(sample);

                        HttpContent byteContent = new StringContent(myContent, Encoding.UTF8, "application/json");
                        byteContent.Headers.ContentType = new MediaTypeHeaderValue("application/json");

                        await Task.Run(async () =>
                        {
                            HttpResponseMessage response = await ThisAddIn.client.PostAsync(
                                "train", byteContent);
                            string responseString = await response.Content.ReadAsStringAsync();
                            JavaScriptSerializer oJS = new JavaScriptSerializer();
                            ResultObj obj = new ResultObj();
                            obj = oJS.Deserialize<ResultObj>(responseString);
                            int flag = int.Parse(obj.Result);
                            if (flag == 1)
                            {
                                MessageBox.Show("Successfully added as negative example in Filter");
                            }
                            else
                            {
                                MessageBox.Show("Some error occured");
                            }
                        });
                    }
                }
            }
            catch (Exception exp)
            {
                Console.WriteLine(exp.Message);
            }
        }
    }
}
