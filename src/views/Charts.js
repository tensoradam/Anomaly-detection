import React from "react";
// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  Row,
  Col
} from "reactstrap";


const Charts = (props) => {
    return (
        <Col className="mb-5 mb-xl-0" xl="12">
            <Card className="shadow">
            <CardHeader className="border-0">
                <Row className="align-items-center">
                  <div className="col">
                    <h3 className="mb-0">Image chart</h3>
                  </div>
                </Row>
              </CardHeader>
              <CardBody>
                {props.plots ?
                <React.Fragment>
                  <p>{props.insights}</p>
                  <img src={require(`../assets/img/${props.plots.isolation_forest}`)} alt="Chart diagram"></img>
                </React.Fragment>
                : <p>The image will appear here...</p>
                }
              </CardBody>
            </Card>
        </Col>
    );
};

export default Charts;