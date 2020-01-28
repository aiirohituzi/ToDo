import Layout from "../components/Layout";
import axios from "axios";

class APITest extends React.Component {
  static async getInitialProps({ req }) {
    const response = await axios.get("http://127.0.0.1:8000/allMemo/");
    return {
      memos: response.data
    };
  }

  addTest = async () => {
    const data = new FormData();

    const memo_obj = JSON.stringify({
      content: "testC",
      isDo: false,
      isStar: false
    });

    data.append("memo", memo_obj);
    data.append("user", "admin");

    const config = {
      // headers: {
      //   "Content-Type": "application/json",
      //   "Access-Control-Allow-Origin": "*"
      // }
      headers: { "content-type": "multipart/form-data" }
    };

    await axios
      .post("http://127.0.0.1:8000/addMemo/", data, config)
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      });
  };

  render() {
    const { memos } = this.props;

    const memoList = memos.map(memo => <li key={memo.id}>{memo.content}</li>);

    return (
      <Layout>
        <ul>{memoList}</ul>
        <button onClick={this.addTest}>Add Test</button>
      </Layout>
    );
  }
}

export default APITest;
