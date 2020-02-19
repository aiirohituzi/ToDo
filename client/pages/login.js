import Layout from "../components/Layout";
import { useState, useEffect } from "react";

const login = () => {
  return (
    <Layout>
      <style>
        {`
          .wrapper-login {
            position: relative;
            background: #00dddd;
            min-width: 200px;
            min-height: 250px;
            width: 20vw;
            height: 25vw;
            top: 20vh;
            margin: auto;
            text-align: center;
          }

          input[type=text] {
            width: 70%;
          }
        `}
      </style>
      <div class="wrapper-login">
        <input type="text" />
        <input type="text" />
      </div>
    </Layout>
  );
};

export default login;
