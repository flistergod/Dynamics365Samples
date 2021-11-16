//called from action - Review Invoices
using Microsoft.Xrm.Sdk;
using Microsoft.Xrm.Sdk.Query;
using Microsoft.Xrm.Sdk.Workflow;
using System;
using System.Activities;
using CrmEarlyBound;
using Microsoft.Xrm.Sdk.Messages;

namespace ReviewInvoices
{
    public class AssignInvoices : CodeActivity
    {
        [RequiredArgument]
        [Input("actualPerson")]
        public InArgument<string> actualPerson { get; set; }

        [RequiredArgument]
        [Input("assignedPerson")]
        public InArgument<string> assignedPerson { get; set; }



        protected override void Execute(CodeActivityContext context)
        {


            ITracingService tracingService = context.GetExtension<ITracingService>();
            IWorkflowContext workflowContext = context.GetExtension<IWorkflowContext>();
            IOrganizationServiceFactory serviceFactory = context.GetExtension<IOrganizationServiceFactory>();
            IOrganizationService svc = serviceFactory.CreateOrganizationService(workflowContext.UserId);

            try
            {
                string currentPerson = actualPerson.Get(context);
                string nextPerson = assignedPerson.Get(context);


                if (currentPerson == null || nextPerson == "" || nextPerson == null || nextPerson == "")
                {

                    tracingService.Trace("Invalid guid");
                    throw new Exception("Invalid GUID");
                }

                else
                {

                    tracingService.Trace("valid guid");

                   

                }

            }
            catch (Exception ex)
            {

                tracingService.Trace("Exception on Review Invoices Activity: {0}", ex.ToString());
            }


        }
    }
}

