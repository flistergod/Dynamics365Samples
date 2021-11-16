using CrmEarlyBound;
using Microsoft.Xrm.Sdk;
using Microsoft.Xrm.Sdk.Query;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Fatura
{
    public class PreCreateChangeName : IPlugin
    {

        //give today's date to dateFatura field
        public void Execute(IServiceProvider serviceProvider)
        {
     
            ITracingService tracingService = (ITracingService)serviceProvider.GetService(typeof(ITracingService));
            IOrganizationServiceFactory serviceFactory = (IOrganizationServiceFactory)serviceProvider.GetService(typeof(IOrganizationServiceFactory));
            IPluginExecutionContext context = (IPluginExecutionContext)serviceProvider.GetService(typeof(IPluginExecutionContext));
            IOrganizationService service = serviceFactory.CreateOrganizationService(context.UserId);

            try
            {

                if (context.InputParameters.Contains("Target") && context.InputParameters["Target"] is Entity)
                {

                    del_fatura entity = ((Entity)context.InputParameters["Target"]).ToEntity<del_fatura>();

                    if (entity.LogicalName != "del_fatura") { return; }

                    var _newDate = DateTime.Today.ToShortDateString();
                 
                    var systemUser = (SystemUser)service.Retrieve(
                           entity.CreatedBy.LogicalName,
                           entity.CreatedBy.Id,
                           new ColumnSet(
                               new String[] { "lastname", "firstname" }
                               )
                           );

                    if (systemUser != null)
                    {
                        var newName = systemUser.FirstName + ' ' + systemUser.LastName;
                        var invoiceFinalName = newName + '_' + _newDate;
                        entity.del_Name = invoiceFinalName;

                    }
                    else { 
                       
                        throw new Exception("could not Retrieve system user"); 

                    }


                }
            }
            catch (Exception ex)
            {

                tracingService.Trace("FaturaChangeName: {0}", ex.ToString());
            }

        }
    }
}
