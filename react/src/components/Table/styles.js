import styled from "styled-components";

export const TableLineColor = styled.td`
background-color: ${(props) => (props.color)};
`;

export const NodeShapes = styled.img`
width: 4vw;
height: 5vh;
background-color: ${(props) => (props.color)};
`;