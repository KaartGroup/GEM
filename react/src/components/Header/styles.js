import styled from "styled-components";

export const AppBar = styled.header`
  font-family: "Hind Guntur", sans-serif;
  font-size: 14px;
  line-height: 1.4285em;
  transition: box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
  box-shadow: 0px 2px 4px -1px rgba(0, 0, 0, 0.2),
    0px 4px 5px 0px rgba(0, 0, 0, 0.14), 0px 1px 10px 0px rgba(0, 0, 0, 0.12);
  width: 100%;
  display: flex;
  z-index: 1100;
  box-sizing: border-box;
  flex-shrink: 0;
  flex-direction: column;
  position: static;
  color: rgba(0, 0, 0, 0.87);
  background-color: #ffffff;
`;

export const Toolbar = styled.div`
  color: rgba(0, 0, 0, 0.87);
  box-sizing: inherit;
  position: relative;
  align-items: center;
  padding-left: 24px;
  padding-right: 24px;
  min-height: 64px;
  width: 100%;
  height: 100%;
  display: flex;
`;
export const Link = styled.a`
align-items: center;
  list-style: none;
  list-style-type: disc;
  line-height: 1em;
  box-sizing: border-box;
  color: black;
  margin: 0;
  padding: 0;
  border: 0;
  outline: 0;
  vertical-align: baseline;
  background: transparent;
  text-decoration: none;
  display: block;
  position: relative;
  text-transform: uppercase;
  font-size: 16px;
  transition: color 300ms ease 0ms;
  padding-bottom: 8px;
  padding-right: 20px;
  &:hover {
    color: #f4753c;
  }
`;
export const ImageIcon = styled.div`
    position: "relative",
    height: 100,
`;

export const KaartLogo = styled.img`
  height: 100px;
  position: relative;
  transition: transform 0.2s;
  &:hover {
    transform: scale(1.2);
  }
`;

export const Icon = styled.span`
  width: 1em;
  height: 1em;
  overflow: hidden;
  font-size: 1.5rem;
  flex-shrink: 0;
  user-select: none;
`;

export const Typography = styled.div`
  flex-grow: 1;
  font-size: 1.25rem;
  font-weight: 500;
  line-height: 1.6;
  letter-spacing: 0.0075em;
`;

export const MenuItem = styled.div`
  background: transparent!important;
  font-weight: 400;
  text-align: left;
  font-family: "Hind Guntur", sans-serif;
  font-size: 14px;
  line-height: 1.4285em;
  color: rgba(0, 0, 0, 0.87);
  box-sizing: inherit;
  display: flex;
`;
