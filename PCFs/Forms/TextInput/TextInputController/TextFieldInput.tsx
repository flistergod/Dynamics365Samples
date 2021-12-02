import * as React from 'react';
import { TextField } from '@fluentui/react/lib/TextField';

interface IState {
    newText : string | null;
}

export interface IProps extends IState{
    text:string|null;
    onChange: (text:string|undefined)=>void;
}

export class TextFieldInput extends React.Component<IProps, IState>{
    constructor(props:IProps){
        super(props)

        this.state={
            newText:this.props.text
        };
    }

    render(){
        return(
            <TextField value={this.state.newText===null ? undefined : this.state.newText} label="Input" 
            onChange={(ev, newText)=>{
                this.setState({newText: newText === undefined ? null : newText});
                this.props.onChange(newText);
            }}
            />
        );
}
}