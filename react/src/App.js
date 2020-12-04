import React from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import {Banner} from './banner';
import { BrowserRouter, Switch, Route } from "react-router-dom";
import './App.css';
import Table from './table';

function App() {
  return (
    <BrowserRouter>
      <Switch>
      <Route path ="/">
      <Header />
      <Table />
      <Banner />
      <Footer />
      </Route>
      </Switch>
      </BrowserRouter>
        );
      }

export default App;