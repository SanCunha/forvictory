import React from 'react';

import Body from './ui/Body.js'

import './index.css';

function Header (){
    return (
        <div className="header">
            FOR VICTORY!
        </div>
    );
}

function Footer (){
    return (
        <div className="footer">Todos os direitos reservados!</div>
    );
}

class App extends React.Component{
    render() {
        return (
            <div className="app">
                <Header/>
                <Body/>
                <Footer/>
            </div>
        );
    }
}
        
export default App;
