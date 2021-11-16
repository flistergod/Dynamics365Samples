using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Xrm.Sdk;
using Microsoft.Xrm.Sdk.Query;
using CrmEarlyBound;

namespace Fatura

{
    public class PreCreateFaturaDate : IPlugin
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
           
                    var _newDate = new DateTime(DateTime.Today.Year, DateTime.Today.Month, DateTime.Today.Year);
                    entity.del_dataFatura = _newDate;

                }
            }
            catch (Exception ex)
            {

                tracingService.Trace("PreCreateChangeDate: {0}", ex.ToString());
            }


        }
    }
}
