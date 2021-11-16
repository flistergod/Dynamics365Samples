// JavaScript source code
aTuaMom={
 changeFieldProperties: function(executionContext) {

    //read form object
    let formContext = executionContext.getFormContext();

    //get estado

    let estado = formContext.getAttribute("del_estado").getValue();

    //if state= reviewed, make all fields read-only
    if (estado === 100000002) {

        aTuaMom.setAllDisabled(formContext);
    }

},

//makes all form fields read-only
 setAllDisabled: function(formContext) {


    formContext.data.entity.attributes.forEach(function (attribute) {
        let control = formContext.getControl(attribute.getName());

        if (control) {
            control.setDisabled(true)
        }
    });
},

addNotificationToFaturaValue: function(executionContext) {
    
    
    let formContext = executionContext.getFormContext();
    let ValorFaturaControl = formContext.getControl('del_valorfatura');
    let ValorFatura = formContext.data.entity.attributes.get('del_valorfatura').getValue();
    let notificationId='ValorFaturaError';

    if (ValorFatura<0) {
        
        let actionCollection = {
            message: 'Insira um valor positivo',
            actions: null
        };

        //actions
        /*
        actionCollection.actions = [function () {
            tickerSymbol.setValue('MSFT');
           
        }];
        */

        ValorFaturaControl.addNotification({
            messages: ['Valor Fatura Inválido'],
            notificationLevel: 'ERROR',
            uniqueId: notificationId,
            actions: [actionCollection]
        });

    
    }else{

        formContext.ui.clearFormNotification(notificationId);
        ValorFaturaControl.clearNotification(notificationId);

    }
},

openDialogEditPerson: function(formContext){

    let personId=formContext.getAttribute("del_cliente").getValue()[0].id.slice(1,-1);
   // var record_name = field.getValue()[0].name;
   // var record_entityName = field.getValue()[0].entityType;

    let pageInput = {
        pageType: "entityrecord",
        entityName: "del_pessoa",
        entityId: personId
    };
    let navigationOptions = {
        target: 2,
        height: {value: 80, unit:"%"},
        width: {value: 70, unit:"%"},
        position: 1,
        title:"Edit Person"
    };
    Xrm.Navigation.navigateTo(pageInput, navigationOptions).then(
        function success() {
                // Run code on success
        },
        function error() {
                // Handle errors
        }
    );   
}

}