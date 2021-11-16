// JavaScript source code
oTeuPai = {
changeFullName2: function(executionContext) {
    console.log("dffdf");
},
changeFullName: function(executionContext) {

    let formContext = executionContext.getFormContext();
    let firstName = formContext.getAttribute("del_name").getValue();
    let lastName = formContext.getAttribute("del_lastname").getValue();

    if (firstName != null && lastName != null) {

        let fullName = firstName + ' ' + lastName;
        formContext.getAttribute("del_fullname").setValue(fullName);
        
}
},


    reviewInvoices: function(formContext) {

    let personId = formContext.data.entity.getId();
    oTeuPai.callGlobalAction(personId);

},


    callGlobalAction: function(personId) {
   
    try {

        var parameters = {};
        parameters.PessoaId = personId;

        var req = new XMLHttpRequest();
        req.open("POST", Xrm.Utility.getGlobalContext().getClientUrl() + "/api/data/v9.1/del_ReviewInvoices", true);
        req.setRequestHeader("OData-MaxVersion", "4.0");
        req.setRequestHeader("OData-Version", "4.0");
        req.setRequestHeader("Accept", "application/json");
        req.setRequestHeader("Content-Type", "application/json; charset=utf-8");

        req.onreadystatechange = function () {
            if (this.readyState === 4) {
                req.onreadystatechange = null;
                if (this.status === 204) {
                } else {
                    Xrm.Utility.alertDialog(this.statusText);
                }
            }
        };
        req.send(JSON.stringify(parameters));
    }
    catch (ex) {
        Xrm.Navigation.openErrorDialog({ message: ex.message, details: ex.message });
    }

},

    faturaFastCreate: function(formContext) {

    let clientId = formContext.data.entity.getId().slice(1, -1);
    let clientName = formContext.getAttribute("del_fullname").getValue();
    let formEntityLogicalName = formContext.data.entity.getEntityName();
    let subGridEntityLogicalName = formContext.getControl("faturas").getEntityName();

    let entityFormOptions = {};
    entityFormOptions["entityName"] = subGridEntityLogicalName; //del_fatura
    entityFormOptions["useQuickCreateForm"] = true;

    let formParameters = {};
    formParameters["del_estado"] = "100000000";

    
    var today = new Date();
    var date = (today.getMonth()+1)+'/'+today.getDate()+'/'+today.getFullYear();
    formParameters["del_datafatura"] = date;

    var clientLookup = new Array();
    clientLookup[0] = new Object();
    clientLookup[0].id = clientId;
    clientLookup[0].name = clientName;
    clientLookup[0].entityType = formEntityLogicalName;

    // Set lookup column
    //find_cliente
    formParameters["del_cliente"] = clientLookup; // ID of the user.
    //  formParameters["find_clientename"] = clientName // Name of the user.
    //  formParameters["find_clientetype"] = formEntityLogicalName//"systemuser"; // Table name.


    // Open the form.
    Xrm.Navigation.openForm(entityFormOptions, formParameters).then(
        function (success) {
            console.log(success);
        },
        function (error) {
            console.log(error);
        });

},

getReviewedInvoice: function(formContext){

    let count = formContext.getAttribute("del_reviewedinvoices").getValue();

    if(count>0){
        return true;
    }
    else{
        return false;
    }

},

refreshRibbon: function(formContext){

    formContext.ui.refreshRibbon(refreshAll);

},



tabGeneralStateChange: function(executionContext){

    let message='Informacoes desta tab são restritas';
    let level='WARNING';
    let uniqueId='BackEndTabWarning';
    let arg="BackEnd";
    let formContext=executionContext.getFormContext();
    let tabObj = formContext.ui.tabs.get(arg);

    tabObj.addTabStateChange(
        
        function onTabChange(){
           
            let formContext=executionContext.getFormContext();
            let tabObj = formContext.ui.tabs.get(arg);
            let displayState=tabObj.getDisplayState();
      
            if(displayState=="expanded"){

                formContext.ui.setFormNotification(message, level, uniqueId);
            }
            else{
        
                formContext.ui.clearFormNotification(uniqueId)
            }
        
    });
    
},

removeEventListeners: function(executionContext){

    let formContext=executionContext.getFormContext();
    let arg="BackEnd";
    let message='Informacoes desta tab são restritas';
    let level='WARNING';
    let uniqueId='BackEndTabWarning';
    let tabObj = formContext.ui.tabs.get(arg);
    let displayState=tabObj.getDisplayState();
    tabObj.removeTabStateChange(

    function onTabChange(){
           
        if(displayState=="expanded"){

            formContext.ui.setFormNotification(message, level, uniqueId);
        }
        else{
    
            formContext.ui.clearFormNotification(uniqueId)
        }
    });

},

assignInvoices: function(formContext){

    let formEntityLogicalName=formContext.data.entity.getEntityName();
    let _defaultViewId='PessoaView';
    let _viewIds=oTeuPai.getViews();

    
    let lookupOptions = 
            {
                allowMultiSelect: false,
                defaultEntityType: formEntityLogicalName,
                defaultViewId:_defaultViewId,
                disableMru: true,
                entityTypes: [formEntityLogicalName],
                //filters: [{filterXml: "<filter type='or'><condition attribute='name' operator='like' value='A%' /></filter>",entityLogicalName: "account"}]
                searchText:"",
                showBarcodeScanner: true,
                viewIds:_viewIds
                
            };

    Xrm.Utility.lookupObjects(lookupOptions).then(
        function(success){
  
        let actualPerson=formContext.data.entity.getId().slice(1,-1);
        let assignedPerson=success[0].id.slice(1,-1);

        oTeuPai.callGlobalAction2(actualPerson, assignedPerson);
        },

        function(error){console.log(error);});

},

getViews: function(){

    let _viewIds=[];

    var req = new XMLHttpRequest();
    req.open("GET", Xrm.Utility.getGlobalContext().getClientUrl() + "/api/data/v9.1/savedqueries?$select=name,returnedtypecode,savedqueryid&$filter=returnedtypecode eq 'undefined'&$orderby=name asc", true);
    req.setRequestHeader("OData-MaxVersion", "4.0");
    req.setRequestHeader("OData-Version", "4.0");
    req.setRequestHeader("Accept", "application/json");
    req.setRequestHeader("Content-Type", "application/json; charset=utf-8");
    req.setRequestHeader("Prefer", "odata.include-annotations=\"*\",odata.maxpagesize=5");
    req.onreadystatechange = function() {
        if (this.readyState === 4) {
            req.onreadystatechange = null;
            if (this.status === 200) {
                var results = JSON.parse(this.response);
                for (var i = 0; i < results.value.length; i++) {
                 
                    var savedqueryid = results.value[i]["savedqueryid"];
                    _viewIds.push(savedqueryid);
                }
                return _viewIds;
            } else {
                Xrm.Utility.alertDialog(this.statusText);
            }
        }
    };
    req.send();
},


callGlobalAction2: function(actualPerson, assignedPerson){

    try {

        var parameters = {};
        parameters.actualPerson = actualPerson;
        parameters.assignedPerson = assignedPerson;

        var req = new XMLHttpRequest();
        req.open("POST", Xrm.Utility.getGlobalContext().getClientUrl() + "/api/data/v9.1/del_AssignInvoices", true);
        req.setRequestHeader("OData-MaxVersion", "4.0");
        req.setRequestHeader("OData-Version", "4.0");
        req.setRequestHeader("Accept", "application/json");
        req.setRequestHeader("Content-Type", "application/json; charset=utf-8");

        req.onreadystatechange = function () {
            if (this.readyState === 4) {
                req.onreadystatechange = null;
                if (this.status === 204) {
                } else {
                    Xrm.Utility.alertDialog(this.statusText);
                }
            }
        };
        req.send(JSON.stringify(parameters));
    }
    catch (ex) {
        Xrm.Navigation.openErrorDialog({ message: ex.message, details: ex.message });
    }

}
}


