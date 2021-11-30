import React, { useEffect, useState } from "react";
import {
    Input,
    InputGroup,
    Stack,
} from "@chakra-ui/core";


export function RenderPreds(){
    const res = fetch(`http://localhost:9000/analyze?input=https://twitter.com/en/privacy`, {method : 'GET', body : JSON.stringify(newTodo})
    const targets = res.keys
    const paragraphs = []
    for (const k in targets){
                paragraphs = paragraphs.concat(
                'We found {k} tracking in the following paragraphs:')
                for (const p in targets.k){
                    paragraphs = paragraphs.concat(p)
                 }}

    return(
        <div>
          <p>{res}</p>
        </div>)
    }

export function GetPreds(){
  const [item, setItem] = React.useState("")

  const handleInput = event  => {
    setItem(event.target.value)
  }

  const handleSubmit = async (event) => {
    fetch(`http://localhost:9000/analyze?input=https://twitter.com/en/privacy`, {method : 'GET'}).then(RenderPreds)
    }

  return (
    <form onSubmit={handleSubmit}>
      <InputGroup size="md">
        <Input
          pr="4.5rem"
          type="text"
          placeholder= "PLACEHOLDER"
          aria-label="https://twitter.com/en/privacy"
          onChange={handleInput}
        />
      </InputGroup>
    </form>
  )}