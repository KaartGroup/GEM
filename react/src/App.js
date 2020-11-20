import React from 'react';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
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