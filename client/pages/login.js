import Layout from "../components/Layout";
import { useState, useEffect } from "react";
import axios from "axios";

const login = () => {
  const [result, setResult] = useState("default");

  const login = async () => {
    let id = document.getElementById("id").value;
    let pw = document.getElementById("pw").value;
    console.log(id, pw);

    const data = new FormData();

    data.append("username", id);
    data.append("password", pw);

    const config = {
      headers: { "content-type": "multipart/form-data" }
    };

    await axios
      .post("http://127.0.0.1:8000/signIn/", data, config)
      .then(response => {
        setResult(response);
      })
      .catch(error => {
        console.log(error);
      });
  };

  return (
    <Layout>
      <style>
        {`
          .wrapper-login {
            position: relative;
            background: #ff9000;
            border-radius: 5px;
            box-shadow: 10px 10px 5px #555;
            width: 300px;
            height: 400px;
            top: 20vh;
            margin: auto;
            text-align: center;
          }

          .wrapper-login .login-title {
            padding-top: 10%;
            height: 35%;
          }

          .input-group {
            width: 80%;
            margin: auto;
            margin-bottom: 20px;
            text-align: right;
          }

          .input-group span {
            width: 10%;
            margin-right: 10px;
          }

          input#id, #pw {
            bottom: 0px;
            width: 70%;
            height: 30px;
          }

          .button-group {
            width: 100%;
          }

          .button-group button{
            border-radius: 5px;
            width: 35%;
            height: 30px;
            font-size: smaller;
            margin: 3%;
          }
        `}
      </style>
      <div class="wrapper-login">
        <div class="login-title">
          <h2>로그인</h2>
        </div>
        <div class="input-group">
          <span>ID </span>
          <input id="id" type="text" />
        </div>
        <div class="input-group">
          <span>PW </span>
          <input id="pw" type="text" />
        </div>
        <div class="button-group">
          <button onClick={() => login()}>로그인</button>
          <button>회원가입</button>
        </div>
      </div>
      <div>{result}</div>
    </Layout>
  );
};

export default login;
