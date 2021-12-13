import React from "react";
import { render } from 'react-dom';
import { ThemeProvider } from "@chakra-ui/core";

import Header from "./components/Header";
import Todos from "./components/Todos";  // new

function App() {
  return (
    <ThemeProvider>
      <Header />
      <Todos />  {/* new */}
    </ThemeProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)