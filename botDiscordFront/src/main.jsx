import React from 'react'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import App from './App.jsx'
import './index.css'

import ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import Login from './components/pages/login/Login.jsx'
import Home from './components/pages/Home/Home.jsx';
import AuthWrapper from './utils/AuthWrapper.jsx';

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
  }
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>,
);