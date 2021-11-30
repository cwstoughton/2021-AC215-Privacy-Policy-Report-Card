import React from "react";
import { render } from 'react-dom';
import { ThemeProvider } from "@chakra-ui/core";

import Header from "./components/Header";
import AddTodos from "./components/Todos";  // new

function App() {
  return (
    <ThemeProvider>
      <Header />
      <AddTodos />  {/* new */}
    </ThemeProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)