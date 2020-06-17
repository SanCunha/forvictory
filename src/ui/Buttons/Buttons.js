import React from 'react'

import Button from 'react-bootstrap/Button'

import './buttons.css'

const Buttons = () => {
    return (
        <div className="buttons">
            <Button variant="primary" style={{width: 25 + '%'}} >CORNERS </Button>
            <Button variant="primary" style={{width: 25 + '%'}} >FILTER </Button>
            <Button variant="primary" style={{width: 25 + '%'}} >BET </Button>
        </div>
    );
}

export default Buttons;