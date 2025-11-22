import axios from "axios";
import React, { useState } from "react";
// reactstrap components
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  Container,
  Row,
  Col,
  Input,
  Table
} from "reactstrap";
import Header from "../components/Headers/Header.js";
// import responseFile from "../response.json";

const Index = (props) => {
  const [selectedFile, updateSelectedFile] = useState(null);
  const [summary, updateSummary] = useState('');
  const [insights, updateInsights] = useState('');
  const [plots, updatePlots] = useState('');
  const [data, updateData] = useState({});
  const [step, updateStep] = useState(1);
  const [chartImg, setChartImg] = useState('');
  
  const onFileChange = (event) => {
    updateSelectedFile(event.target.files[0])
  };

  const analyse = () => {
    updateStep(3);
  }

  const home = () => {
    updateStep(1);
  }

  const onFileUpload = () => {
    // Create an object of formData
    const formData = new FormData();
    // Update the formData object
    formData.append(
        "myFile",
        selectedFile,
        selectedFile.name
    );

    // Details of the uploaded file
    console.log(selectedFile);

    // Request made to the backend api
    // Send formData object
    axios.post("http://localhost:5000/api/uploadfile", formData, {
      headers: {
        "content-type": "multipart/form-data",
      },
    }).then(function (response) {
      updateData(response.data.data.isolation_forest)
      updatePlots(response.data.plots)
      updateInsights(response.data.insights);
      updateSummary(response.data.summary);
      setChartImg(`data:image/jpeg;base64,${response.data.plots.isolation_forest}`)
      updateStep(2);
    }).catch(function (error) {
      console.log(error);
      // let data = responseFile;
      // updateData(data.data.isolation_forest)
      // updatePlots(data.plots)
      // updateInsights(data.insights);
      // updateSummary(data.summary);
      // updateStep(2);
    });;
  };

  const renderStep = () => {
    switch (step) {
        case 1:
            return (
              <Col className="mb-5 mb-xl-0" xl="12">
                <Card className="bg-gradient-default shadow">
                  <CardHeader className="bg-transparent">
                    <Row className="align-items-center">
                      <div className="col">
                        <h6 className="text-uppercase text-light ls-1 mb-1">
                          Upload the CSV file
                        </h6>
                        <h3 className="text-white mb-0">Detection</h3>
                      </div>
                    </Row>
                  </CardHeader>
                  <CardBody>                    
                  <Row className="align-items-right">
                      <div className="col">
                        <Input
                          type="file"
                          onChange={onFileChange}
                        />
                        <br></br>
                        <Button onClick={onFileUpload}>Upload</Button>
                      </div>
                    </Row>                  
                  </CardBody>
                </Card>
              </Col>
            );
        case 2:
            return (
              <Col className="mb-5 mb-xl-0" xl="12">
                <Card className="shadow">
                    <CardHeader className="border-0">
                        <Row className="align-items-center">
                            <Col xs="8">
                                <h3 className="mb-0">Detected result</h3>
                            </Col>
                            <Col className="text-right" xs="4">
                                <Button
                                    color="primary"
                                    href="#analyse"
                                    onClick={() =>analyse()}
                                    size="sm"
                                >
                                    Analyse
                                </Button>
                            </Col>
                        </Row>
                    </CardHeader>
                    {data?.length > 1 ?
                        <React.Fragment>
                            <p className="ml-4">{summary}</p>
                            <Table className="align-items-center table-flush" responsive>
                                <thead className="thead-light">
                                    <tr>
                                        <th scope="col">Offer_description</th>
                                        <th scope="col">Sales</th>
                                        <th scope="col">Profit</th>
                                        <th scope="col">Score</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {data.map((item, index) => (
                                        <tr key={index}>
                                            <th scope="row">{item.Offer_description}</th>
                                            <td>{item.Sales}</td>
                                            <td>{item.Profit}</td>
                                            <td>{item.anomaly_score_isolation_forest}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </Table>
                        </React.Fragment>
                        : <p className="col ml-2"> The result will come here.. </p>
                    }
                </Card>
            </Col>
            );
        case 3:
            return (
              <Col className="mb-5 mb-xl-0" xl="12">
                <Card className="shadow">
                <CardHeader className="border-0">
                    <Row className="align-items-center">
                      <Col xs="8">
                        <h3 className="mb-0">Image chart</h3>
                      </Col>
                      <Col className="text-right" xs="4">
                        <Button
                            color="primary"
                            href="#home"
                            onClick={() =>home()}
                            size="sm"
                        >
                            Home
                        </Button>
                      </Col>
                    </Row>
                  </CardHeader>
                  <CardBody>
                    {chartImg != '' ?
                    <React.Fragment>
                      <p>{insights}</p>
                      <img src={chartImg} alt="Chart diagram"></img>
                    </React.Fragment>
                    : <p>The image will appear here...</p>
                    }
                  </CardBody>
                </Card>
              </Col>
            );
        default:
            return null;
    }
  };
  return (
    <>
      <Header />
      {/* Page content */}
      <Container className="mt--7 body-content mb-2" fluid>
        <Row>
          <p>fgdfgsd</p>{step}
          {renderStep()}
        </Row>
      </Container>
    </>
  );
};

export default Index;
