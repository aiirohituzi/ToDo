import Layout from "../components/Layout";
import { useState, useEffect } from "react";
import axios from "axios";

const ToDoList = () => {
  const [list, setList] = useState();

  const getAllMemo = async () => {
    await axios
      .get("http://127.0.0.1:8000/allMemo/")
      .then(response => {
        console.log(response.data);
        setList(response.data);
      })
      .catch(error => {
        console.log(error);
      });
  };

  useEffect(() => {
    getAllMemo();
  }, []);

  return (
    <div>
      <style>
        {`
          .wrapper-list {
          }
        `}
      </style>
      <div class="wrapper-list">
        <ul>
          {list
            ? list.map(item => {
                return <li>{item.content}</li>;
              })
            : "빈 값"}
        </ul>
      </div>
    </div>
  );
};

export default ToDoList;
