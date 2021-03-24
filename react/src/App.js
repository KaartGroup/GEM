 import React from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { Gem } from "./components/GEM";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import { DataProvider } from "common/DataContext";
import './App.css';


function App() {


  return (
    <BrowserRouter>
    <DataProvider>
      <Switch>
      <Route path ="/">
       <Header /> 
        <Gem />
       <Footer /> 
       </Route> 
      </Switch>
      </DataProvider>
      </BrowserRouter>
        );
      }

export default App;