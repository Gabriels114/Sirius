import styled, {css, keyframes} from "styled-components";

interface SkeletonProps {
    width: number | string
    height: number | string
    $variant: 'circular' | 'rectangular' | 'h1' | 'h3' | 'body' | 'caption' | 'text'
    $animation?: false | 'wave'
    color?: string
    className?: string
    id?: string
}

const wave$animation = keyframes`
    100% {
    background-position: calc(-100%) 0;
  }
  0% {
    background-position: calc(100%)  0;
  }
`

const blink$animation = keyframes`
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
`

export const SkeletonStyled = styled.div<SkeletonProps>`
  display: inline-block;
  background-color: ${({ color }) => color || "var(--background)"};
  border-radius: 3px;
  ${({ $variant }) => {
    switch ($variant) {
      case "circular":
        return `
          border-radius: 50%;
        `;
      case "h1":
        return `
          height: 32px;
          width: 60%;
        `;
      case "h3":
        return `
          height: 24px;
          width: 50%;
        `;
      case "body":
        return `
          height: 16px;
          width: 100%;
        `;
      case "caption":
        return `
          height: 12px;
          width: 70%;
        `;
      case "text":
        return `
            height: 14px;
            width: 90%;
        `;
    default:
        return `
            border-radius: 4px;
        `;
    }
    }}
    ${({ width }) => width && `width: ${typeof width === "number" ? `${width}px` : width};`}
    ${({ height }) => height && `height: ${typeof height === "number" ? `${height}px` : height};`}

    ${({ $animation }) =>
    $animation === "wave" ?
    css`
        background-image: linear-gradient(
        90deg,
        var(--wave-start) 25%,
        var(--wave-middle) 50%,
        var(--wave-start) 75%
        );
        background-size: 200% 100%;
        animation: ${wave$animation} 1.5s ease-in-out infinite;
    ` :
    css `
        animation: ${blink$animation} 1.5s ease-in-out infinite;
    `}
`

export default function Skeleton(props: SkeletonProps) {
    return <SkeletonStyled {...props} />;
}