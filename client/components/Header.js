import Link from "next/link";

const linkStyle = {
  marginRight: "1rem"
};
const Header = () => {
  return (
    <div>
      <Link href="/">
        <a style={linkStyle}>홈</a>
      </Link>
      <Link href="/about">
        <a style={linkStyle}>소개</a>
      </Link>
      <Link href="/ssr-test">
        <a prefetch style={linkStyle}>
          SSR 테스트
        </a>
      </Link>
      <Link href="/api-test">
        <a prefetch style={linkStyle}>
          API 테스트
        </a>
      </Link>
      <Link href="/dragAnimation">
        <a style={linkStyle}>드래그 애니메이션</a>
      </Link>
      <Link href="/login">
        <a style={linkStyle}>로그인</a>
      </Link>
      <Link href="/toDoList">
        <a style={linkStyle}>전체 목록 보기</a>
      </Link>
    </div>
  );
};

export default Header;
