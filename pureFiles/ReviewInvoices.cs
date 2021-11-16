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
    public class ReviewInvoices : CodeActivity
    {
        [RequiredArgument]
        [Input("PessoaId")]
        public InArgument<string> PessoaId { get; set; }

       

        protected override void Execute(CodeActivityContext context)
        {

        
            ITracingService tracingService = context.GetExtension<ITracingService>();
            IWorkflowContext workflowContext = context.GetExtension<IWorkflowContext>();
            IOrganizationServiceFactory serviceFactory = context.GetExtension<IOrganizationServiceFactory>();
            IOrganizationService svc = serviceFactory.CreateOrganizationService(workflowContext.UserId);

            try
            {
                string pessoaId = PessoaId.Get(context);


                if (pessoaId == null || pessoaId == "") {

                    tracingService.Trace("Invalid guid");
                    throw new Exception("Invalid GUID"); 
                }

                else
                {

                    tracingService.Trace("valid guid");

                    /*
                    var pessoaRecord = (del_pessoa)svc.Retrieve(
                    del_pessoa.EntityLogicalName,
                    Guid.Parse(pessoaId),
                    new ColumnSet(
                    new String[] { "name", "del_pessoaId" }
                    ));
                    */

                    // Define Condition Values
                    var query_del_estado = 100000002;
                    var query_del_cliente = pessoaId;

                    // Instantiate QueryExpression query
                    var query = new QueryExpression("del_fatura");

                    // Add columns to query.ColumnSet
                    query.ColumnSet.AddColumns("del_faturaid", "del_cliente", "del_estado");

                    // Define filter query.Criteria
                    query.Criteria.AddCondition("del_estado", ConditionOperator.NotEqual, query_del_estado);
                    query.Criteria.AddCondition("del_cliente", ConditionOperator.Equal, query_del_cliente);


                    DataCollection<Entity> faturas = svc.RetrieveMultiple(query).Entities;

                    tracingService.Trace("get faturas");


                    if (faturas.Count > 0)
                    {
                        tracingService.Trace(">0 faturas");

                        // Create an ExecuteMultipleRequest object.
                        var multipleRequest = new ExecuteMultipleRequest()
                        {
                            // Assign settings that define execution behavior: continue on error, return responses. 
                            Settings = new ExecuteMultipleSettings()
                            {
                                ContinueOnError = false,
                                ReturnResponses = true
                            },
                            // Create an empty organization request collection.
                            Requests = new OrganizationRequestCollection()
                        };


                        foreach (Entity entity in faturas)
                        {
                            del_fatura fatura = (del_fatura)entity;
                            // Console.WriteLine("Retrieved Opportunity Product {0}", fatura.del_estado);
                            tracingService.Trace("fatura.del_estado: {0}", fatura.del_estado);
                            fatura.del_estado = del_fatura_del_estado.Revista;

                            UpdateRequest updateRequest = new UpdateRequest { Target = entity };
                            multipleRequest.Requests.Add(updateRequest);
                        }

                        tracingService.Trace("num requests "+ multipleRequest.Requests.Count);

                        ExecuteMultipleResponse multipleResponse = (ExecuteMultipleResponse)svc.Execute(multipleRequest);

                    }

                    else {
                        
                        throw new Exception("no del_fatura  non reviewed records associated with this client"); 
                    }

                }

            }
            catch (Exception ex)
            {

                tracingService.Trace("Exception on Review Invoices Activity: {0}", ex.ToString());
            }
           

        }
    }
}  
    
