import React from 'react';
import { Header } from '../src/header';
import { Footer } from './footer';
import {Banner} from './banner';
import './App.css';
import Table from './table';

function App() {
  return (
    <div className="Main Site">
      <Header />
      <Table />
      <Banner />
      <Footer />
      </div>
        );
      }

export default App;