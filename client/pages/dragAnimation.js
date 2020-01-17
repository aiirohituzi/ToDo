import Layout from "../components/Layout";
import { useState, useEffect } from "react";

const DragAnimation = () => {
  const down = e => {
    console.log(e);
    e.target.style.background = "#fff";
    e.target.style.position = "fixed";
    e.target.addEventListener("mousemove", move);
    // e.target.addEventListener("mouseup", up);
  };

  const move = e => {
    console.log(e.target);
    e.target.style.top = e.clientX - 5;
    // e.target.style.top = '10vw';
    e.target.style.left = e.clientX - 5;
  };

  const up = e => {
    console.log(e);
    e.target.style.background = "#f99";
    e.target.style.removeProperty("position");
    e.target.style.removeProperty("top");
    e.target.style.removeProperty("left");

    e.target.removeEventListener("mousemove", move);
    e.target.removeEventListener("mouseup", up);
  };

  useEffect(() => {
    console.log(document.querySelector("li"));
    document.querySelector("li").addEventListener("mousedown", down);
    // return document.querySelector("li").removeEventListener("mousedown", down);
  }, []);
  return (
    <Layout>
      <style>
        {`
          ul {
            list-style: none;
          }
          li {
            width: 20vw;
            margin: 3px;
            padding: 5px;
            background: #f99;
            border: 1px solid #f00;
            border-radius: 5px;
            cursor: pointer;
          }
          li:hover {
            background: #f55;
          }
        `}
      </style>
      <ul>
        <li>List 1</li>
        <li>List 2</li>
        <li>List 3</li>
        <li>List 4</li>
        <li>List 5</li>
      </ul>
    </Layout>
  );
};

export default DragAnimation;
