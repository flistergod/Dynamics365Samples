/*
*This is auto generated from the ControlManifest.Input.xml file
*/

// Define IInputs and IOutputs Type. They should match with ControlManifest.
export interface IInputs {
    DropZoneID: ComponentFramework.PropertyTypes.StringProperty;
    OtherDropZoneIDs: ComponentFramework.PropertyTypes.StringProperty;
    IsMasterZone: ComponentFramework.PropertyTypes.TwoOptionsProperty;
    DroppedSource: ComponentFramework.PropertyTypes.StringProperty;
    DroppedTarget: ComponentFramework.PropertyTypes.StringProperty;
    DroppedId: ComponentFramework.PropertyTypes.StringProperty;
    DroppedBeforeId: ComponentFramework.PropertyTypes.StringProperty;
    ItemBackgroundColour: ComponentFramework.PropertyTypes.StringProperty;
    ItemFontSize: ComponentFramework.PropertyTypes.DecimalNumberProperty;
    ItemFontColour: ComponentFramework.PropertyTypes.StringProperty;
    items: ComponentFramework.PropertyTypes.DataSet;
}
export interface IOutputs {
    DroppedSource?: string;
    DroppedTarget?: string;
    DroppedId?: string;
    DroppedBeforeId?: string;
}
