import React from 'react'

import Buttons from '../ui/Buttons/Buttons.js'
import Display from './Display/Display.js'

import Card from 'react-bootstrap/Card'
import ListGroup from 'react-bootstrap/ListGroup'
import Button from 'react-bootstrap/Button'

import './ui.css'


const Body = () => {
    return (
        <div className="body">
            <div className="left_menu">
            <Card>
                <Card.Body style={{padding: 0 + 'px'}} variant="card-body">
                    <Card.Title as="h3">Leagues</Card.Title>
                    <ListGroup variant="flush">
                        <ListGroup.Item style={{padding: 0 + 'px'}}> 
                            <Button variant="primary btn-block">England Premier League </Button>
                        </ListGroup.Item>
                    </ListGroup>
                </Card.Body>
            </Card>
            </div>
            <div className="display">
                <Buttons/>
                <Display/>
            </div>
        </div>
    );
}

export default Body;