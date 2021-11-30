import React from "react";
import { render } from 'react-dom';
import { ThemeProvider } from "@chakra-ui/core";

import Header from "./components/Header";
import { RenderPreds } from "./components/Todos2";
import { GetPreds } from "./components/Todos2";  // new

function App() {
  return (
    <ThemeProvider>
      <Header />
      <GetPreds />
      <RenderPreds />
    </ThemeProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)