using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Web.Script.Serialization;
using System.Threading.Tasks;
using System.Windows.Forms;
using Microsoft.Office.Tools.Ribbon;

using Newtonsoft.Json;

namespace SmartFilterAddin
{
    public partial class Form1 : Form
    {
        public class FilterObject
        {
            public FilterObject(string filterName)
            {
                this.filterName = filterName;
            }

            public string filterName { get; set;  }
        }
        public Form1()
        {
            InitializeComponent();
        }

        private async void button1_ClickAsync(object sender, EventArgs e)
        {
            if (textBox1.Text != null)
            {
                
                string filterName = textBox1.Text;
                ThisAddIn.listOfFilters.Add(textBox1.Text);
                
                RibbonDropDownItem item = Globals.Ribbons.Ribbon1.Factory.CreateRibbonDropDownItem();
                item.Label = textBox1.Text;
                Globals.Ribbons.Ribbon1.dropDown1.Items.Add(item);

                this.Close();

                // send createfilter API
                try
                {
                    // Create a new product
                    FilterObject filterObject = new FilterObject(filterName);
                    var myContent = JsonConvert.SerializeObject(filterObject);

                    HttpContent byteContent = new StringContent(myContent, Encoding.UTF8, "application/json");
                    byteContent.Headers.ContentType = new MediaTypeHeaderValue("application/json");
                   
                    await Task.Run(async () =>
                    {
                        HttpResponseMessage response = await ThisAddIn.client.PostAsync(
                         "createFilter", byteContent);
                        if( response.StatusCode == System.Net.HttpStatusCode.OK)
                        {
                            // Success case
                            MessageBox.Show("Sent request to server to create model with your filter");
                        }
                        else
                        {
                            // Failure case
                            MessageBox.Show("Something went wrong!. Receieved response code "+ response.StatusCode+" from server");
                        }
                    });

                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
            else
            {
                MessageBox.Show("You entered nothing!");
                this.Close();
            }
        }
    }
}
