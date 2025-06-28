import React from "react";
import { render, screen } from "@testing-library/react";
import App from "../src/App.jsx";

test("renders Vite + React heading", () => {
    render(<App />);
    const headingElement = screen.getByText(/vite \+ react/i);
    expect(headingElement).toBeInTheDocument();
});
