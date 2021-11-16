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
    public class PreCreateUpdateLastInvoice : IPlugin
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

                   
                    var query = new QueryExpression("del_fatura");
                    query.TopCount = 1;
                    query.ColumnSet.AddColumns("del_faturaid", "del_estado");
                    query.AddOrder("createdon", OrderType.Descending);

                    del_fatura secondLastRecord = (del_fatura)service.RetrieveMultiple(query).Entities[0];

                    if (secondLastRecord!=null) {

                        secondLastRecord.del_estado = del_fatura_del_estado.Acabada;
                        service.Update(secondLastRecord);
                    }
                    else { 
                        throw new Exception("could not retrive last fatura"); 
                    }
                    
                }
            }
            catch (Exception ex)
            {

                tracingService.Trace("PreCreateUpdateLastInvoice: {0}", ex.ToString());
            }
        }
    }
}
