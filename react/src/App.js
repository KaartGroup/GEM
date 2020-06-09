import React from 'react';
import { Header } from '../src/header';
import { Footer } from './footer';
import {Banner} from './banner';
import './App.css';

function App() {
  return (
    <div className="Main Site">
      <Header />
      <Banner />
      <Footer />
      <p>My Token = {window.token}</p>
      </div>
        );
      }

export default App;