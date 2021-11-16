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
    public class PreCreateUpdateNotifyAge : IPlugin
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

                    del_pessoa entity = ((Entity)context.InputParameters["Target"]).ToEntity<del_pessoa>();

                    if (entity.LogicalName != "del_pessoa") { return; }


                    DateTime _now = DateTime.Now;
                    DateTime dataNascimento = (DateTime)entity.del_dataNasc;
                    var totalDays = (_now - dataNascimento).TotalDays;
                    var totalYears = Math.Truncate(totalDays / 365);
                    var totalMonths = Math.Truncate((totalDays % 365) / 30);
                    var remainingDays = Math.Truncate((totalDays % 365) % 30);
                    var preOperation = context.MessageName;

                    tracingService.Trace("Estimated age is {0} year(s), {1} month(s) and {2} day(s)", totalYears, totalMonths, remainingDays);

                    if (totalYears < 18)
                    {

                        throw new InvalidPluginExecutionException($"Idade inferior a 18 anos. Ação não permitida - {preOperation}");

                    }

                }
            }
            catch (Exception ex)
            {

                tracingService.Trace("PreCreatePerson Age exception: {0}", ex.ToString());
                throw new InvalidPluginExecutionException(ex.Message);
            }

        }
    }
}
