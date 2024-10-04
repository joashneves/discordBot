import React from 'react'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import './index.css'

import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import Login from './components/pages/login/Login.jsx'
import Home from './components/pages/Home/Home.jsx';
import AuthWrapper from './utils/AuthWrapper.jsx';
import Franquias from './components/pages/Persona/Franquias.jsx'
import PersonagemLista from './components/pages/PersonagemLista/PersonagemLista.jsx';

const router = createBrowserRouter([{
  path: "/", // Páginas protegidas
  element: 
      <Login />,
  },{
    path: "/Home", // Páginas protegidas
    element: (
      <AuthWrapper>
        <Home />
        </AuthWrapper>
    ),
  },{
    path: "/Persona", // Páginas protegidas
    element: (
      <AuthWrapper>
        <Franquias />
        </AuthWrapper>
    ),
  },{
    path: "/personagens/:id", // Páginas protegidas
    element: (
      <AuthWrapper>
        <PersonagemLista />
        </AuthWrapper>
    ),
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
);