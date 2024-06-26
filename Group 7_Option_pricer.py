# -*- coding: utf-8 -*-
"""
testing pyQt5
python 3.9
PyQt5==5.15.7
scipy==1.7.1
"""

import sys
import math
from math import sqrt, log, exp, isnan, ceil
import numpy as np
import scipy.stats
from scipy.stats import norm, mstats, qmc
import pandas as pd

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Option pricer")

        self.layoutc0 = QVBoxLayout()
        self.layoutc0.setSpacing(2)

        self.layouth1 = QHBoxLayout()
        self.layoutc1 = QVBoxLayout()
        self.layoutc2 = QVBoxLayout()
        self.layoutc3 = QVBoxLayout()
        self.layoutc4 = QVBoxLayout()

        self.layouth1.setContentsMargins(0, 0, 0, 0)
        self.layouth1.setSpacing(2)

        # left column
        self.widget0 = QLabel("Hi user, Here are some user guidance:\n        1. Choose an option type below\n\
        2. Input the parameters that show up\n        3. Click the “Execute” button\n\
        4. Collect the results based on your selection\nHave fun and wish you luck!")
        self.widget0.setStyleSheet("border : 2px solid black;")
        self.widget0.setWordWrap(True)

        self.widget11_1 = QLabel(
            "\nSelect types of option product to be priced")

        self.widget11 = QComboBox()
        self.widget11.addItems(["---Select your pricing model---",
                                "European Option (Closed form)",
                                "Implied Volatility (European Option)",
                                "Geometric Asian Option (Closed form)",
                                "Geometric Basket Option (2 assets) (Closed form)",
                                "KIKO Put Option (Quasi MC)",
                                "Asian Option (MC Method)",
                                "Basket Option (2 assets) (MC Method)",
                                "American Option (Binomial Tree)",
                                ])

        self.widget12_1 = QLabel("Select Call/Put")
        self.widget12 = QComboBox()
        self.widget12.addItems(["Call", "Put"])

        self.widget13 = QLabel("User Reminder:")
        self.widget13.setStyleSheet("border : 2px solid black;")
        self.widget13.setWordWrap(True)

        self.widget1end = QLabel("      ")

        self.widgetslist1 = [self.widget0, self.widget11_1, self.widget11,
                             self.widget12_1, self.widget12, self.widget13,
                             self.widget1end]

        for w in self.widgetslist1:
            self.layoutc1.addWidget(w)

        self.layouth1.addLayout(self.layoutc1)

        # Middle column
        self.widget21_1 = QLabel("Spot Price (S)")
        self.widget21 = QLineEdit()

        self.widget22_1 = QLabel("Strike Price (K)")
        self.widget22 = QLineEdit()

        self.widget23_1 = QLabel("Time to Maturity (T) (in year, e.g. 1=1year)")
        self.widget23 = QLineEdit()

        self.widget24_1 = QLabel(
            "Interest Rate (r) (in decimal, e.g. 0.1=10%)")
        self.widget24 = QLineEdit()

        self.widget25_1 = QLabel(
            "Volatility (sigma) (in decimal, e.g. 0.1=10%)")
        self.widget25 = QLineEdit()

        self.widget26_1 = QLabel("No. of tree steps (N_steps)")
        self.widget26 = QLineEdit()

        self.widget27_1 = QLabel("Option Price (V)")
        self.widget27 = QLineEdit()

        self.widget28_1 = QLabel("Repo Rate (q) (in decimal, e.g. 0.1=10%)")
        self.widget28 = QLineEdit()

        # Asian option input boxes
        self.widget2asian_11 = QLabel("No. of observation periods (n)")

        # Basket input boxes
        self.widget2bkt_11 = QLabel("Spot Price 1st asset (S1)")

        self.widget2bkt_21 = QLabel("Spot Price 2nd asset (S2)")
        self.widget2bkt_2 = QLineEdit()

        self.widget2bkt_31 = QLabel(
            "Sigma 1st asset (Sigma1) (in decimal, e.g. 0.1=10%)")

        self.widget2bkt_41 = QLabel(
            "Sigma 2nd asset (Sigma2) (in decimal, e.g. 0.1=10%)")
        self.widget2bkt_4 = QLineEdit()

        self.widget2bkt_51 = QLabel("correlation (rho) (between [-1,1])")
        self.widget2bkt_5 = QLineEdit()

        # KIKO input boxes
        self.widget2KIKO_11 = QLabel("Lower barrier (L)")
        self.widget2KIKO_1 = QLineEdit()

        self.widget2KIKO_21 = QLabel("Upper barrier (U)")
        self.widget2KIKO_2 = QLineEdit()

        self.widget2KIKO_31 = QLabel("No. of observation periods (N)")

        self.widget2KIKO_41 = QLabel("Cash rebate ratio (CR)")
        self.widget2KIKO_4 = QLineEdit()

        # MC option
        self.widget2MC_11 = QLabel("No. of simulation paths (M)")
        self.widget2MC_1 = QLineEdit()

        # covariate option
        self.widget2Covmethod = QCheckBox(
            'if pricing Arithm, select if use covariate method (tick:Yes/untick:No)')
        self.widget2Covmethod.setCheckState(Qt.Checked)
        # changing position of indicator
        self.widget2Covmethod.setLayoutDirection(Qt.RightToLeft)

        # Geometric/Arithmetic
        self.widget2geoarithm = QCheckBox(
            'Select if pricing based on Arithm/Geom (tick:Arithm/untick:Geom)')
        self.widget2geoarithm.setCheckState(Qt.Checked)
        # changing position of indicator
        self.widget2geoarithm.setLayoutDirection(Qt.RightToLeft)

        # end space for column
        self.widget2end = QLabel("     ")

        # generate a list of widget in the 2nd column
        self.widgetslist2 = [self.widget21_1, self.widget2bkt_11, self.widget21,
                             self.widget22_1, self.widget22,
                             self.widget23_1, self.widget23,
                             self.widget24_1, self.widget24,
                             self.widget25_1, self.widget2bkt_31,  self.widget25,
                             self.widget26_1, self.widget2asian_11, self.widget2KIKO_31, self.widget26,
                             self.widget27_1, self.widget27,
                             self.widget28_1,  self.widget28,
                             self.widget2bkt_21, self.widget2bkt_2,
                             self.widget2bkt_41, self.widget2bkt_4,
                             self.widget2bkt_51, self.widget2bkt_5,
                             self.widget2KIKO_11, self.widget2KIKO_1,
                             self.widget2KIKO_21, self.widget2KIKO_2,
                             self.widget2KIKO_41, self.widget2KIKO_4,
                             self.widget2MC_11, self.widget2MC_1,
                             self.widget2geoarithm, self.widget2Covmethod,
                             self.widget2end]

        for w in self.widgetslist2:
            self.layoutc2.addWidget(w)

        self.layouth1.addLayout(self.layoutc2)

        # Right column
        self.widget31 = QPushButton('Execute pricing')
        self.widget31.clicked.connect(lambda: self.button_oppricer())

        self.widget31_1 = QLabel('')
        
        self.widget32 = QLabel("Results")

        self.widget33_1 = QLabel("Option price")
        self.widget33_2 = QLabel("")

        self.widget33 = QLineEdit()

        self.widget34_1 = QLabel("Implied vol. from option price")
        self.widget34_2 = QLabel("")

        self.widget34 = QLineEdit()

        self.widget35_1 = QLabel("95% confidence interval")
        self.widget35 = QLineEdit()

        self.widget3mid = QLabel("     ")

        self.widget37 = QPushButton('Quit window.')
        self.widget37.clicked.connect(lambda: self.close())

        self.widget3end = QLabel("     ")

        self.widgetslist3 = [self.widget31, self.widget31_1 , self.widget32,
                             self.widget33_1, self.widget34_1, self.widget33_2, self.widget33,
                             self.widget35_1, self.widget35,
                             self.widget3mid, self.widget37,   self.widget3end]

        for w in self.widgetslist3:
            self.layoutc3.addWidget(w)

        self.layouth1.addLayout(self.layoutc3)

        # add a table at the bottom
        self.widget41_1 = QLabel("Calculation History")
        self.widget41 = QTableWidget()
        self.widgetslist4 = [self.widget41_1, self.widget41]

        for w in self.widgetslist4:
            self.layoutc4.addWidget(w)

        # self.layouth1.addLayout(self.layoutc4)
        self.layoutc0.addLayout(self.layouth1)
        self.layoutc0.addLayout(self.layoutc4)

        self.widget = QWidget()
        # self.widget.setLayout(self.layouth1)
        self.widget.setLayout(self.layoutc0)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(self.widget)
        # Connect the currentIndexChanged signal of the widget11 QComboBox to the update_widgets method
        self.widget11.currentIndexChanged.connect(self.update_widgets)

        # Connect the currentIndexChanged signal of the widget11 QComboBox to the update_widgets method
        self.widget2geoarithm.stateChanged.connect(
            self.update_widgets_arithm_geom)

        # Hide all widgets in widgetslist2 initially
        for widget in self.widgetslist2:
            widget.hide()

        # Hide selected widgets in column 3

        self.widgets_col3_initialhidelist = [self.widget33_1, self.widget34_1,  self.widget33_2, self.widget33,

                                             self.widget35_1, self.widget35]

        for widget3 in self.widgets_col3_initialhidelist:
            widget3.hide()

    def show_warning_messagebox(self, msgcontent):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        warnpara = 'Input error(s) is found as below, please check:'
        for warnsent in msgcontent:
            warnpara = warnpara + '\n' + warnsent

        # setting message for Message Box (inputs from verifyinputfcn)
        msg.setText(warnpara)

        # setting Message box window title
        msg.setWindowTitle("Warning: Errors in input are found.")

        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)

        # go back to the pricer
        retval = msg.exec_()

    def show_warning_messagebox_product(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        # setting message for Message Box (inputs from verifyinputfcn)
        msg.setText('You have not select an option product.')

        # setting Message box window title
        msg.setWindowTitle("Reminder: Please select an option product.")

        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)

        # go back to the pricer
        retval = msg.exec_()

    # Define a new method to update the visibility of widgets based on the selected option
    def update_widgets_arithm_geom(self):

        # create contents in edit text box everytime.
        self.widget2Covmethod.hide()

        if (self.widget2geoarithm.isChecked()):
            self.widget2Covmethod.show()
        else:
            self.widget2Covmethod.hide()

    # Define a new method to update the visibility of widgets based on the selected option
    def update_widgets(self):

        # create contents in edit text box everytime.
        self.widgetsedittextboxlist2 = [self.widget21,
                                        self.widget22,
                                        self.widget23,
                                        self.widget24,
                                        self.widget25,
                                        self.widget26,
                                        self.widget27,
                                        self.widget28,
                                        self.widget2bkt_2,
                                        self.widget2bkt_4,
                                        self.widget2bkt_5,
                                        self.widget2KIKO_1,
                                        self.widget2KIKO_2,
                                        self.widget2KIKO_4,
                                        self.widget2MC_1,
                                        self.widget33,
                                        self.widget34,
                                        self.widget35]

        for widget in self.widgetsedittextboxlist2:
            widget.setText('')

        # default setting
        self.widget2geoarithm.setChecked(True)
        self.widget2Covmethod.setChecked(True)
        
        # clear text whenever change to another option product
        self.widget31_1.setText('')
        self.widget33_2.setText('')
        self.widget34_2.setText('')
               
        # clear the table
        self.widget41.clear()
        self.widget41.setRowCount(0)

        for widget in self.widgetslist2:
            widget.hide()

        for widget3 in self.widgets_col3_initialhidelist:
            widget3.hide()

        self.optionproduct = self.widget11.currentText()
        # Hide widget27_1 and widget27 if "European Option (closed form)" is selected
        if self.optionproduct == "European Option (Closed form)":

            # option type choice avialable except for KIKO put
            self.widget12_1.show()
            self.widget12.show()

            self.widget21_1.show()
            self.widget21.show()
            self.widget22_1.show()
            self.widget22.show()
            self.widget23_1.show()
            self.widget23.show()
            self.widget24_1.show()
            self.widget24.show()
            self.widget25_1.show()
            self.widget25.show()
            self.widget28_1.show()
            self.widget28.show()
            self.widget2end.show()

            self.widget33_1.show()
            self.widget33_2.show()
            self.widget33.show()

            self.widget13.setText("User reminder:")
            self.widget41.setColumnCount(8)
            self.widget41.setHorizontalHeaderLabels(
                ['S', 'K', 'sigma', 'T', 'r', 'q', 'optype', 'Price'])

        elif self.optionproduct == "Implied Volatility (European Option)":

            # option type choice avialable except for KIKO put
            self.widget12_1.show()
            self.widget12.show()

            self.widget21_1.show()
            self.widget21.show()
            self.widget22_1.show()
            self.widget22.show()
            self.widget23_1.show()
            self.widget23.show()
            self.widget24_1.show()
            self.widget24.show()
            self.widget27_1.show()
            self.widget27.show()
            self.widget28_1.show()
            self.widget28.show()
            self.widget2end.show()

            self.widget34_1.show()
            self.widget33_2.show()
            self.widget33.show()

            self.widget13.setText(
                "User reminder: The option price(V) must be greater than its intrinsic value, but smaller than discounted asset price(call option) or discounted strike price(put option).")
            self.widget41.setColumnCount(8)
            self.widget41.setHorizontalHeaderLabels(
                ['S', 'K', 'V', 'T', 'r', 'q', 'optype', 'Implied Vol.'])

        elif self.optionproduct == "Geometric Asian Option (Closed form)":

            # option type choice avialable except for KIKO put
            self.widget12_1.show()
            self.widget12.show()

            self.widget21_1.show()
            self.widget21.show()
            self.widget22_1.show()
            self.widget22.show()
            self.widget23_1.show()
            self.widget23.show()
            self.widget24_1.show()
            self.widget24.show()
            self.widget25_1.show()
            self.widget25.show()
            self.widget2asian_11.show()
            self.widget26.show()
            self.widget2end.show()

            self.widget33_1.show()
            self.widget33_2.show()
            self.widget33.show()

            self.widget13.setText(
                "User reminder: Number of observation periods must be a positive integer.")
            self.widget41.setColumnCount(8)
            self.widget41.setHorizontalHeaderLabels(
                ['S', 'K', 'T', 'r', 'sigma','N', 'optype', 'Price'])
            # S, K, T, r, sigma, totsteps, optype, opstyle='European'):

        elif self.optionproduct == "American Option (Binomial Tree)":

            # option type choice avialable except for KIKO put
            self.widget12_1.show()
            self.widget12.show()

            self.widget21_1.show()
            self.widget21.show()
            self.widget22_1.show()
            self.widget22.show()
            self.widget23_1.show()
            self.widget23.show()
            self.widget24_1.show()
            self.widget24.show()
            self.widget25_1.show()
            self.widget25.show()
            self.widget26_1.show()
            self.widget26.show()
            self.widget2end.show()

            self.widget33_1.show()
            self.widget33_2.show()
            self.widget33.show()

            self.widget13.setText(
                "User reminder: Number of tree steps must be a positive integer.")
            self.widget41.setColumnCount(8)
            self.widget41.setHorizontalHeaderLabels(
                ['S', 'K', 'T', 'r', 'sigma','N_steps', 'optype', 'Price'])
            #self, S, K, T, r, sigma, totsteps, optype, opstyle='American'

        elif self.optionproduct == "Geometric Basket Option (2 assets) (Closed form)":

            # option type choice avialable except for KIKO put
            self.widget12_1.show()
            self.widget12.show()

            self.widget2bkt_11.show()
            self.widget21.show()
            self.widget22_1.show()
            self.widget22.show()
            self.widget23_1.show()
            self.widget23.show()
            self.widget24_1.show()
            self.widget24.show()
            self.widget2bkt_31.show()
            self.widget25.show()
            self.widget2bkt_21.show()
            self.widget2bkt_2.show()
            self.widget2bkt_41.show()
            self.widget2bkt_4.show()
            self.widget2bkt_51.show()
            self.widget2bkt_5.show()
            self.widget2end.show()

            self.widget33_1.show()
            self.widget33_2.show()
            self.widget33.show()

            self.widget13.setText(
                "User reminder: correlation rho is defined as the price correlation between the two assets.")
            self.widget41.setColumnCount(10)
            self.widget41.setHorizontalHeaderLabels(
                ['S1', 'K', 'T', 'r', 'sigma1', 'S2', 'Sigma2', 'rho', 'optype', 'Price'])

        elif self.optionproduct == "Asian Option (MC Method)":

            # option type choice avialable except for KIKO put
            self.widget12_1.show()
            self.widget12.show()

            self.widget21_1.show()
            self.widget21.show()
            self.widget22_1.show()
            self.widget22.show()
            self.widget23_1.show()
            self.widget23.show()
            self.widget24_1.show()
            self.widget24.show()
            self.widget25_1.show()
            self.widget25.show()
            self.widget2asian_11.show()
            self.widget26.show()
            self.widget2MC_11.show()
            self.widget2MC_1.show()
            self.widget2geoarithm.show()
            self.widget2Covmethod.show()
            self.widget2end.show()

            self.widget33_1.show()
            self.widget33_2.show()
            self.widget33.show()

            self.widget35_1.show()
            self.widget35.show()

            self.widget13.setText(
                "User reminder: Due to inaccurate result for small M (<1e2) while long calculation time for large M (>1e5), please select M between 100 and 100000")
            
            self.widget41.setColumnCount(12)
            self.widget41.setHorizontalHeaderLabels(
                ['S', 'K', 'T', 'r', 'sigma','N', 'M','optype', 'Price','2.5% C.I.', '97.5% C.I.' ,'Cal_MC_methods'])
            
        elif self.optionproduct == "Basket Option (2 assets) (MC Method)":

            # option type choice avialable except for KIKO put
            self.widget12_1.show()
            self.widget12.show()

            self.widget2bkt_11.show()
            self.widget21.show()
            self.widget22_1.show()
            self.widget22.show()
            self.widget23_1.show()
            self.widget23.show()
            self.widget24_1.show()
            self.widget24.show()
            self.widget2bkt_31.show()
            self.widget25.show()
            self.widget2bkt_21.show()
            self.widget2bkt_2.show()
            self.widget2bkt_41.show()
            self.widget2bkt_4.show()
            self.widget2bkt_51.show()
            self.widget2bkt_5.show()
            self.widget2MC_11.show()
            self.widget2MC_1.show()
            self.widget2geoarithm.show()
            self.widget2Covmethod.show()
            self.widget2end.show()

            self.widget33_1.show()
            self.widget33_2.show()
            self.widget33.show()

            self.widget35_1.show()
            self.widget35.show()

            self.widget13.setText(
                "User reminder: Due to inaccurate result for small M (<1e2) while long calculation time for large M (>1e5), please select M between 100 and 100000")
            self.widget41.setColumnCount(14)
            self.widget41.setHorizontalHeaderLabels(
                ['S1', 'K', 'T', 'r', 'Sigma1', 'S2', 'Sigma2', 'rho','M', 'optype', 'Price','2.5% C.I.', '97.5% C.I.','Cal_MC_methods'])

        elif self.optionproduct == "KIKO Put Option (Quasi MC)":
            self.widget21_1.show()
            self.widget21.show()
            self.widget22_1.show()
            self.widget22.show()
            self.widget23_1.show()
            self.widget23.show()
            self.widget24_1.show()
            self.widget24.show()
            self.widget25_1.show()
            self.widget25.show()
            self.widget2KIKO_31.show()
            self.widget26.show()
            self.widget2KIKO_11.show()
            self.widget2KIKO_1.show()
            self.widget2KIKO_21.show()
            self.widget2KIKO_2.show()
            self.widget2KIKO_41.show()
            self.widget2KIKO_4.show()
            self.widget2MC_11.show()
            self.widget2MC_1.show()
            self.widget2end.show()

            # No option type choice for KIKO Put
            self.widget12_1.hide()
            self.widget12.hide()

            self.widget33_1.show()
            self.widget33_2.show()
            self.widget33.show()

            self.widget35_1.show()
            self.widget35.show()

            self.widget13.setText(
                "User reminder: Due to inaccurate result for small M (<1e2) while long calculation time for large M (>1e5), please select M between 100 and 100000")
            self.widget41.setColumnCount(14)
            self.widget41.setHorizontalHeaderLabels(
                ['S', 'K', 'T', 'r', 'sigma','L', 'U','CR','M', 'N', 'optype', 'Price','2.5% C.I.', '97.5% C.I.'])
        else:
            for w in self.widgetslist2:
                w.hide()
            for widget3 in self.widgets_col3_initialhidelist:
                widget3.hide()

            self.widget13.setText("User reminder:")

    def button_oppricer(self):

        self.optionproduct = self.widget11.currentText()

        # First check whether input parameters are correct:
        if (self.optionproduct == "---Select your pricing model---"):
            self.show_warning_messagebox_product()
            return
        else:
            verifyinput, msgtobereturn = self.verifyinputfcn()
        
        self.widget31_1.setText('')
        # set as red colour
        
        ### msgtobereturn=['Stock price S(0)/S1(0) must not be blank and be positive.','Strike price S(0)/S1(0) must not be blank and be positive.']
        # verifyinput=False

        if (verifyinput == True):

            # collect inputs and turn them as numeric values

            # S1(0) for asset 1 for Basket type; otherwise S(0) for all remaining types
            self.S = float(self.widget21.text())
            self.K = float(self.widget22.text())       # strike price
            self.T = float(self.widget23.text())       # Time to maturity
            self.r = float(self.widget24.text())       # interest rate

            # sigma1 for asset 1 in Basket type; otherwise S(0) for all remaining option types
            if self.optionproduct == "Implied Volatility (European Option)":
                self.sigma = None
            else:
                self.sigma = float(self.widget25.text())
            # collect option types
            self.optype = self.widget12.currentText()

            # initially additional parameters for other option types are all set as None
            self.price = None                      # only in implied vol
            self.q = None                          # only in vanila European options

            # Asian or KIKO:  observation steps; American : tree steps
            self.totsteps = None
            self.S2 = None                         # only in basket
            self.sigma2 = None                     # only in basket
            self.rho = None                        # only in basket
            self.M = None                          # MC simulation paths
            self.barrier_lower = None              # only in KIKO
            self.barrier_upper = None              # only in KIKO
            self.CR = None

            if self.optionproduct == "European Option (Closed form)":
                self.q = float(self.widget28.text())

            if self.optionproduct == "Implied Volatility (European Option)":
                self.price = float(self.widget27.text())
                self.q = float(self.widget28.text())

            # collect additional inputs only if needed
            if self.optionproduct == "American Option (Binomial Tree)":
                self.totsteps = int(self.widget26.text())

            elif self.optionproduct == "Geometric Asian Option (Closed form)" or self.optionproduct == "Asian Option (MC Method)":
                self.totsteps = int(self.widget26.text())
                if self.optionproduct == "Asian Option (MC Method)":
                    self.M = int(self.widget2MC_1.text())

            elif self.optionproduct == "Geometric Basket Option (2 assets) (Closed form)" or self.optionproduct == "Basket Option (2 assets) (MC Method)":
                self.S2 = float(self.widget2bkt_2.text())
                self.sigma2 = float(self.widget2bkt_4.text())
                self.rho = float(self.widget2bkt_5.text())
                if self.optionproduct == "Basket Option (2 assets) (MC Method)":
                    self.M = int(self.widget2MC_1.text())

            elif self.optionproduct == 'KIKO Put Option (Quasi MC)':
                self.totsteps = int(self.widget26.text())
                self.barrier_lower = float(self.widget2KIKO_1.text())
                self.barrier_upper = float(self.widget2KIKO_2.text())
                self.CR = float(self.widget2KIKO_4.text())
                self.M = int(self.widget2MC_1.text())
            else:
                pass
            
            ### add reminder to user that their inputs on these parameters are as intended.
            if ((self.sigma is not None) and (self.sigma>=1)) or (self.T>=100) or (self.r>=1) or ((self.sigma2 is not None) and (self.sigma2>=1)) or  ((self.q is not None) and (self.q>=1)):
               self.widget31_1.setText('Reminder: T is in year while sigma(s),r,q are in decimial.')
             
        else:
            self.show_warning_messagebox(msgtobereturn)
            return

        ###
        if (verifyinput == True):

            if (self.optionproduct == 'European Option (Closed form)'):
                self.opprice_bsEU = self.black_scholes(
                    self.S, self.K, self.T, self.sigma, self.r, self.q, self.optype)
                self.widget33_2.setText(str('European')+' '+self.optype)
                self.widget33.setText(
                    "{:.6f}".format(float(self.opprice_bsEU)))

                self.add_line_eu(self.S, self.K, self.sigma, self.T,
                                 self.r, self.q, self.optype, self.opprice_bsEU)

            elif (self.optionproduct == 'Implied Volatility (European Option)'):
                 
                #### first check whether the option price is inside the theoretical range:   
                msgtobereturnimpvol=[]
                if self.optype=='Call':
                        uppertheoryrange=self.S*exp(-1*self.q*self.T)
                        lowertheoryrange=max(self.S*exp(-1*self.q*self.T)-self.K*exp(-1*self.r*self.T),0)
                        if (self.price>uppertheoryrange) or (self.price<lowertheoryrange):
                           msgtobereturnimpvol.append("The input price for the call option is outside the theoretical range [{:.6f} , {:.6f}].".format(float(lowertheoryrange), float(uppertheoryrange)))
                           self.show_warning_messagebox(msgtobereturnimpvol)
                           self.widget33.setText('Implied vol not applicable.')
                           return 
                    
                else:
                        uppertheoryrange=self.K*exp(-1*self.r*self.T)
                        lowertheoryrange=max(self.K*exp(-1*self.r*self.T)-self.S*exp(-1*self.q*self.T),0)
                        if (self.price>uppertheoryrange) or (self.price<lowertheoryrange):
                           msgtobereturnimpvol.append("The input price for the put option is outside the theoretical range [{:.6f} , {:.6f}].".format(float(lowertheoryrange), float(uppertheoryrange)))
                           self.show_warning_messagebox(msgtobereturnimpvol)
                           self.widget33.setText('Implied vol not applicable.')
                           return
                
                
                self.opprice_implied_vol = self.implied_vol(
                    self.price, self.S, self.K, self.T, self.r, self.q, self.optype)
                self.widget33_2.setText(
                    str('Implied Volatility') + ' ' + self.optype)
                if self.opprice_implied_vol == 'The Newton-Raphson method did not converge.':
                    self.widget33.setText(self.opprice_implied_vol)
                    msgtobereturnimpvol.append('The Newton-Raphson method did not converge.')
                    self.show_warning_messagebox(msgtobereturnimpvol)

                else:
                    self.widget33.setText("{:.6f}".format(
                        float(self.opprice_implied_vol)))
                    self.add_line_eu(self.S, self.K, self.price, self.T,
                                     self.r, self.q, self.optype, self.opprice_implied_vol)

            elif (self.optionproduct == 'Geometric Asian Option (Closed form)'):
                self.opprice_geo_asian = self.geometric_asian_option_price(
                    self.S, self.K, self.T, self.r, self.sigma, self.totsteps, self.optype)
                self.widget33_2.setText(
                    str('Geometric Asian closed form') + ' ' + self.optype)
                self.widget33.setText("{:.6f}".format(
                    float(self.opprice_geo_asian)))
                self.add_line_eu(self.S, self.K, self.T,
                                     self.r,self.sigma, self.totsteps, self.optype, self.opprice_geo_asian)

            elif (self.optionproduct == 'Geometric Basket Option (2 assets) (Closed form)'):
                self.opprice_geo_basketcf = self.Basket_Geo(
                    self.S, self.S2, self.K, self.T,  self.sigma, self.sigma2, self.r, self.rho, self.optype)
                self.widget33_2.setText(
                    str('Geometric Basket (2 assets) closed form') + ' ' + self.optype)
                self.widget33.setText("{:.6f}".format(
                    float(self.opprice_geo_basketcf)))
                self.add_line_eu(self.S, self.K, self.T,
                                     self.r,self.sigma, self.S2, self.sigma2, self.rho,self.optype,  self.opprice_geo_basketcf)
                #'S1', 'K', 'T', 'r', 'sigma1', 'S2', 'Sigma2', 'rho', 'optype', 'Price'
                #S1, S2, K, T, sigma1, sigma2, r, rho, optype)

            elif (self.optionproduct == 'American Option (Binomial Tree)'):
                self.opstyle = 'American'
                self.opprice_american = self.binotree(
                    self.S, self.K, self.T, self.r, self.sigma, self.totsteps, self.optype, self.opstyle)
                self.widget33_2.setText(str('American')+' '+self.optype)
                self.widget33.setText("{:.6f}".format(
                    float(self.opprice_american)))
                self.add_line_eu(self.S, self.K, self.T,
                                     self.r,self.sigma, self.totsteps, self.optype, self.opprice_american)

            elif (self.optionproduct == 'Asian Option (MC Method)'):
                if (self.widget2geoarithm.isChecked()):
                    self.arithmchosen =True
                    calapproachstr='Arithmetic '
                    # check if use MC covariate method
                    if (self.widget2Covmethod.isChecked()):
                        self.covmethod = True
                        strcovmethod = 'MC with covariate method'
                        self.MC_prod_type='AM_MC_cov'
                    else:
                        self.covmethod = False
                        strcovmethod = 'simple MC method'
                        self.MC_prod_type='AM_MC_simple'
                else:
                    calapproachstr='Geometric '
                    self.arithmchosen = False
                    self.covmethod = True    # does not uee it for this option anyway
                    strcovmethod = 'simple MC method'
                    self.MC_prod_type='GM_MC_simple'
                
                self.opprice_mean_asianmc, self.opprice_std_asianmc, self.oppricelowrange_asianmc, self.oppriceuprange_asianmc = self.Asian_arith_control(
                    self.S, self.K, self.T, self.totsteps, self.sigma, self.r, self.M, self.optype, self.arithmchosen, self.covmethod)
                self.widget33_2.setText(
                    calapproachstr + 'Asian ' + strcovmethod + ' ' + self.optype)
                self.widget33.setText("{:.6f}".format(
                    float(self.opprice_mean_asianmc)))

                self.widget35.setText("({:.6f} , {:.6f})".format(
                    float(self.oppricelowrange_asianmc), float(self.oppriceuprange_asianmc)))
                self.add_line_eu(self.S, self.K, self.T, self.r,self.sigma, self.totsteps,self.M,self.optype ,self.opprice_mean_asianmc, self.oppricelowrange_asianmc, self.oppriceuprange_asianmc, self.MC_prod_type) 

            elif (self.optionproduct == 'Basket Option (2 assets) (MC Method)'):

                if (self.widget2geoarithm.isChecked()):
                    self.arithmchosen = True
                    calapproachstr='Arithmetic '
                    # check if use MC covariate method
                    if (self.widget2Covmethod.isChecked()):
                        self.covmethod = True
                        strcovmethod = 'MC with covariate method'
                        self.MC_prod_type='AM_MC_cov'
                    else:
                        self.covmethod = False
                        strcovmethod = 'simple MC method'
                        self.MC_prod_type='AM_MC_simple'
                else:
                    calapproachstr='Geometric '
                    self.arithmchosen = False
                    self.covmethod = True    # does not uee it for this option anyway
                    strcovmethod = 'simple MC method'
                    self.MC_prod_type='GM_MC_simple'

                self.opprice_mean_basketmc, self.opprice_std_basketmc, self.oppricelowrange_basketmc, self.oppriceuprange_basketmc = self.Basket_arith(
                    self.S, self.S2, self.K, self.T, self.sigma, self.sigma2, self.r, self.rho, self.M, self.optype, self.arithmchosen, self.covmethod)
                self.widget33_2.setText(
                    calapproachstr + 'Basket (2 assets case) ' + strcovmethod + ' ' + self.optype)
                self.widget33.setText("{:.6f}".format(
                    float(self.opprice_mean_basketmc)))

                self.widget35.setText("({:.6f} , {:.6f})".format(
                    float(self.oppricelowrange_basketmc), float(self.oppriceuprange_basketmc)))
                self.add_line_eu(self.S, self.K, self.T, self.r,self.sigma, self.S2, self.sigma2, self.rho,self.M,self.optype, self.opprice_mean_basketmc,self.oppricelowrange_basketmc, self.oppriceuprange_basketmc, self.MC_prod_type)
                #['S1', 'K', 'T', 'r', 'sigma1', 'S2', 'Sigma2', 'rho','M', 'optype', 'Price'])

            elif (self.optionproduct == 'KIKO Put Option (Quasi MC)'):
                
                self.optype='put'
                
                # KIKO option must be a put option
                self.opprice_mean_KIKO, self.oppricelowrange_KIKO, self.oppriceuprange_KIKO = self.KIKO_PUT(
                    self.r, self.sigma, self.T, self.S, self.K, self.barrier_lower, self.barrier_upper, self.totsteps, self.CR, self.M)
                self.widget33_2.setText('KIKO (quasi-MC) put option')
                self.widget33.setText("{:.6f}".format(
                    float(self.opprice_mean_KIKO)))

                self.widget35.setText("({:.6f} , {:.6f})".format(
                    float(self.oppricelowrange_KIKO), float(self.oppriceuprange_KIKO)))
                self.add_line_eu(self.S, self.K, self.T,
                                     self.r,self.sigma,self.barrier_lower, self.barrier_upper,self.CR, self.M, self.totsteps, self.optype, self.opprice_mean_KIKO, self.oppricelowrange_KIKO, self.oppriceuprange_KIKO)
                 #['S', 'K', 'T', 'r', 'sigma','L', 'U','CR','M', 'optype', 'Price'])

            else:
                print(
                    'Unknown option products. Please choose products from within the list.')

    def binotree(self, S, K, T, r, sigma, totsteps, optype, opstyle='American'):

        # parameters from CRR formula
        nointv = T/totsteps
        DF = exp(-r*nointv)

        u = exp(sigma*sqrt(nointv))
        d = 1/u
        p_up = (exp(r*nointv)-d)/(u-d)

        # matrix approach for faster step calculation
        noup = np.arange(totsteps+1)
        noup = np.resize(noup, (totsteps+1, totsteps+1))
        nodown = np.transpose(noup)

        upstep = u**(noup-nodown)
        downstep = d**(nodown)

        # Securities price matrix
        Spricemat = S*upstep*downstep

        # replace lower triangle of the matrix as NaN to avoid confusion
        Spricemat[np.tril_indices(Spricemat.shape[0], -1)] = np.nan

        # Assume no dividend paying feature, American Call should be priced in the same way as European Call.
        if optype.lower() == 'call':
            opprice = np.maximum(Spricemat-K, 0)
            # backwardly solving the present value
            for istep in range(1, totsteps+1):
                opprice[0:totsteps-(istep)+1, totsteps-istep] = (p_up*opprice[0:totsteps-istep+1,
                                                                              totsteps-istep+1]+(1-p_up)*opprice[1:totsteps-(istep-1)+1, totsteps-istep+1])*DF

        elif optype.lower() == 'put':
            if opstyle == 'American':
                colstep = totsteps
                opprice = np.empty((totsteps+1, totsteps+1,))
                opprice[:] = np.nan
                opprice_notex_val = np.empty((totsteps+1, totsteps+1,))
                opprice_notex_val[:] = np.nan

                oppriceex = np.maximum(K-Spricemat, 0)
                opprice[0:totsteps+1, totsteps] = oppriceex[0:totsteps+1, totsteps]
                opprice_notex_val[0:totsteps+1,
                                  totsteps] = oppriceex[0:totsteps+1, totsteps]

                for istep in range(1, totsteps+1):

                    opprice_notex_val[0:totsteps-(istep)+1, totsteps-istep] = (
                        p_up*opprice[0:totsteps-istep+1, totsteps-istep+1]+(1-p_up)*opprice[1:totsteps-(istep-1)+1, totsteps-istep+1])*DF
                    opprice[0:totsteps-(istep)+1, totsteps-istep] = np.maximum(opprice_notex_val[0:totsteps-(
                        istep)+1, totsteps-istep], oppriceex[0:totsteps-(istep)+1, totsteps-istep])

            elif opstyle.lower() == 'European':
                opprice = np.maximum(K-Spricemat, 0)
                # backwardly solving the present value
                for istep in range(1, totsteps+1):
                    opprice[0:totsteps-(istep)+1, totsteps-istep] = (p_up*opprice[0:totsteps-istep+1,
                                                                                  totsteps-istep+1]+(1-p_up)*opprice[1:totsteps-(istep-1)+1, totsteps-istep+1])*DF

        else:
            opprice = np.nan
        return opprice[0, 0]

    def black_scholes(self, S, K, T, sigma, r, q, optype, opstyle='European'):
        d1 = (np.log(S/K) + (r-q) * T) / \
            (sigma * np.sqrt(T)) + 0.5 * (sigma * np.sqrt(T))
        d2 = (np.log(S/K) + (r-q) * T) / \
            (sigma * np.sqrt(T)) - 0.5 * (sigma * np.sqrt(T))

        if optype.lower() == 'call':
            return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif optype.lower() == 'put':
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        else:
            raise ValueError(
                "Invalid option type. Must be either 'call' or 'put'")
    # From Anson

    def implied_vol(self, price, S, K, T, r, q, optype, opstyle='European'):


        try:
            sigmahat = np.sqrt(2 * abs((np.log(S / K) + (r -q) * T) / T))
            tol = 1e-8
            nmax = 1000
            sigmadiff = 1
            n = 1
            sigma = sigmahat
            while sigmadiff >= tol and n < nmax:
                option_price = self.black_scholes(
                    S, K, T, sigma, r, q, optype, opstyle='European')
                d1 = (np.log(S / K) + (r -q) * T) / \
                    (sigma * np.sqrt(T)) + 0.5 * (sigma * np.sqrt(T))
                vega = S * np.exp(-q * T) * np.sqrt(T) * norm.pdf(d1)
                

                increment = (option_price-price) / vega
                if np.isnan(increment) or np.isinf(increment):
                    return "The Newton-Raphson method did not converge."
                    break  
                sigma = sigma-increment
                           
                n = n + 1
                sigmadiff = abs(increment)
            return sigma
        except:
            return "The Newton-Raphson method did not converge."
            #raise ValueError("The Newton-Raphson method did not converge.")

    def geometric_asian_option_price(self, S, K, T, r, sigma, totsteps, optype, opstyle='European'):

        adj_sigma = sigma * \
            np.sqrt((totsteps + 1)*(2*totsteps + 1)/(6*(totsteps**2)))
        adj_mu = (r - 0.5*sigma**2)*(totsteps + 1) / \
            (2*totsteps) + 0.5*adj_sigma**2

        d1 = (np.log(S/K) + (adj_mu + 0.5*adj_sigma**2)*T) / \
            (adj_sigma*np.sqrt(T))
        d2 = d1 - adj_sigma * np.sqrt(T)

        if optype.lower() == 'call':
            return np.exp(-r * T) * (S * norm.cdf(d1) * np.exp(adj_mu*T) - K * norm.cdf(d2))
        else:
            return np.exp(-r * T) * (K * norm.cdf(-d2) - S * norm.cdf(-d1) * np.exp(adj_mu*T))



    def Asian_Geo(self, S, K, T, n, sigma, r, optype):
        sigma_head = sigma*sqrt((n+1)*(2*n+1)/(6*n**2))
        u_head = (r-1/2*sigma**2)*(n+1)/(2*n)+1/2*sigma_head**2

        d1_head = (log(S/K)+(u_head+1/2*sigma_head**2)*T)/(sigma_head*sqrt(T))
        d2_head = d1_head - sigma_head*sqrt(T)

        if optype.lower() == "call":
            V = exp(-r*T)*(S*exp(u_head*T) *
                           norm.cdf(d1_head)-K*norm.cdf(d2_head))
        elif optype.lower() == "put":
            V = exp(-r*T)*(K*norm.cdf(-d2_head)-S *
                           exp(u_head*T)*norm.cdf(-d1_head))
        return V

    def Asian_arith_control(self, S, K, T, n, sigma, r, M, optype, arith = True, control=True):
        self.widget33_2.hide
        Dt = T/n
        payoff = []  # define a list to store the payoffs simulated from asset model
        payoff_geo = []
        E_geo = []
        np.random.seed(7)
        Z = np.random.standard_normal(size=(M, n))
        for i in range(0, M):
            asset_levels = []  # define a list to store the asset levels simulated from asset model
            S_t_j = S
            Z_i = Z[i]
            for j in range(0, n):
                # simulate the asset value at time T, in risk-neutral world
                S_t_j = S_t_j*exp((r-1/2*(sigma**2))*Dt+sigma*sqrt(Dt)*Z_i[j])
                asset_levels.append(S_t_j)

            S_head_T = np.mean(asset_levels)
            S_head_T_geo = mstats.gmean(asset_levels)

            if optype.lower() == "call":
                payoff_i = exp(-r*T)*max(S_head_T - K, 0)
                payoff_geo_i = exp(-r*T)*max(S_head_T_geo - K, 0)
            elif optype.lower() == "put":
                payoff_i = exp(-r*T)*max(K - S_head_T, 0)
                payoff_geo_i = exp(-r*T)*max(K - S_head_T_geo, 0)

            payoff.append(payoff_i)
            payoff_geo.append(payoff_geo_i)
            e_geo_i = self.Asian_Geo(S, K, T, n, sigma, r, optype)
            E_geo.append(e_geo_i)

        E_X_M = np.mean(payoff)
        E_X_M_geo = np.mean(payoff_geo)
        # b_M = 1/M-1 * E((XM-E(XM))^2)
        Var_X_M = M/(M-1) * np.mean((payoff-E_X_M)**2)
        std_error = sqrt(Var_X_M/M)
        conf_low, conf_up = E_X_M - 1.96*std_error, E_X_M + 1.96*std_error
   
        if arith == True:
           if control == True:
               cov_X_Y = np.mean(np.asarray(payoff)*np.asarray(payoff_geo)
                               ) - np.mean(payoff)*np.mean(payoff_geo)
               Var_Y = M/(M-1)*np.mean((payoff_geo - E_X_M_geo)**2)
               payoff_control = np.asarray(
                      payoff) + cov_X_Y/Var_Y*(np.asarray(E_geo) - np.asarray(payoff_geo))
               E_X_M_control = np.mean(payoff_control)
               Var_X_M_control = M / \
                     (M-1)*np.mean((payoff_control - E_X_M_control)**2)
               std_error_control = sqrt(Var_X_M_control/M)
               conf_low_control, conf_up_control = E_X_M_control - 1.96 * \
                    std_error_control, E_X_M_control + 1.96*std_error_control
               return E_X_M_control, std_error_control, conf_low_control, conf_up_control

           elif control == False:
                return E_X_M, std_error, conf_low, conf_up
            
        elif arith == False: #return the Geometric asian option price in MC
           Var_Y = M/(M-1)*np.mean((payoff_geo - E_X_M_geo)**2)
           std_error_Y = sqrt(Var_Y/M)
           conf_low_Y, conf_up_Y = E_X_M_geo - 1.96*std_error_Y, E_X_M_geo + 1.96*std_error_Y
           return E_X_M_geo, std_error_Y, conf_low_Y, conf_up_Y   
            

    def geometric_basket_option_prices(self, S1, S2, K, T, r, sigma1, sigma2, rho, optype="call"):
        sigma_basket = np.sqrt(sigma1**2 + sigma2**2 + 2*sigma1*sigma2*rho)/2
        mu_basket = r - 0.5*(sigma1**2 + sigma2**2)/2 + 0.5*(sigma_basket**2)
        basekt_zero = np.sqrt(S1*S2)
        d1 = (np.log(basekt_zero/K) + (mu_basket + 0.5 *
              sigma_basket**2)*T)/(sigma_basket*np.sqrt(T))
        d2 = d1 - sigma_basket * np.sqrt(T)

        if optype.lower() == 'call':
            return np.exp(-r * T) * (basekt_zero * norm.cdf(d1) * np.exp(mu_basket*T) - K * norm.cdf(d2))
        else:
            return np.exp(-r * T) * (K * norm.cdf(-d2) - basekt_zero * norm.cdf(-d1) * np.exp(mu_basket*T))

    def Basket_Geo(self, S1, S2, K, T, sigma1, sigma2, r, rho, optype):
        sigma_B = sqrt(2*sigma1*sigma2*rho+sigma1 **
                       2+sigma2**2)/2  # need checking
        u_B = r - 1/2*(sigma1**2 + sigma2**2)/2 + 1/2*sigma_B**2
        B_0 = sqrt(S1*S2)
        d1 = (log(B_0/K)+(u_B+1/2*sigma_B**2)*T)/(sigma_B*sqrt(T))
        d2 = d1 - sigma_B*sqrt(T)
        if optype.lower() == "call":
            V = exp(-r*T)*(B_0*exp(u_B*T)*norm.cdf(d1)-K*norm.cdf(d2))
        elif optype.lower() == "put":
            V = exp(-r*T)*(K*norm.cdf(-d2) - B_0*exp(u_B*T)*norm.cdf(-d1))
        return V

    def Basket_arith(self, S1, S2, K, T, sigma1, sigma2, r, rho, M, optype, arith=True, control=True):
        payoff = []
        payoff_geo = []
        E_geo = []
        np.random.seed(7)
        Z1_i = np.random.standard_normal(M)  # generate random number
        np.random.seed(17)
        Z = np.random.standard_normal(M)
        Z2_i = rho*Z1_i + sqrt(1-rho**2)*Z
        for i in range(0, M):
            S1_t_i = S1*exp((r-1/2*(sigma1**2))*T+sigma1*sqrt(T)*Z1_i[i])
            S2_t_i = S2*exp((r-1/2*(sigma2**2))*T+sigma2*sqrt(T)*Z2_i[i])
            B_T = (S1_t_i+S2_t_i)/2
            B_T_geo = sqrt(S1_t_i*S2_t_i)
            if optype.lower() == "call":
                payoff_i = exp(-r*T)*max(B_T-K, 0)  # payoff of call option
                payoff_geo_i = exp(-r*T)*max(B_T_geo-K, 0)
            elif optype.lower() == "put":
                payoff_i = exp(-r*T)*max(K-B_T, 0)  # payoff of put option
                payoff_geo_i = exp(-r*T)*max(K-B_T_geo, 0)
            payoff.append(payoff_i)
            payoff_geo.append(payoff_geo_i)
            e_geo_i = self.Basket_Geo(
                S1, S2, K, T, sigma1, sigma2, r, rho, optype)
            E_geo.append(e_geo_i)
        E_X_M = np.mean(payoff)
        E_X_M_geo = np.mean(payoff_geo)
        Var_X_M = M/(M-1) * np.mean((payoff-E_X_M)**2)
        std_error = sqrt(Var_X_M/M)
        conf_low, conf_up = E_X_M - 1.96*std_error, E_X_M + 1.96*std_error
        
        if arith == True: 
            if control == True:
                cov_X_Y = np.mean(np.asarray(payoff)*np.asarray(payoff_geo)
                               ) - np.mean(payoff)*np.mean(payoff_geo)
                Var_Y = M/(M-1)*np.mean((payoff_geo - E_X_M_geo)**2)
                payoff_control = np.asarray(
                      payoff) + cov_X_Y/Var_Y*(np.asarray(E_geo) - np.asarray(payoff_geo))
                E_X_M_control = np.mean(payoff_control)
                Var_X_M_control = M / \
                    (M-1)*np.mean((payoff_control - E_X_M_control)**2)
                std_error_control = sqrt(Var_X_M_control/M)
                conf_low_control, conf_up_control = E_X_M_control - 1.96 * \
                         std_error_control, E_X_M_control + 1.96*std_error_control
                return E_X_M_control, std_error_control, conf_low_control, conf_up_control

            elif control == False:
               return E_X_M, std_error, conf_low, conf_up
        elif arith == False: #return the Geometric basket option price in MC
            Var_Y = M/(M-1)*np.mean((payoff_geo - E_X_M_geo)**2)
            std_error_Y = sqrt(Var_Y/M)
            conf_low_Y, conf_up_Y = E_X_M_geo - 1.96*std_error_Y, E_X_M_geo + 1.96*std_error_Y
            return E_X_M_geo, std_error_Y, conf_low_Y, conf_up_Y
       

    def KIKO_PUT(self, r, sigma, T, s, K, barrier_lower, barrier_upper, N, R, M):
        if s >= barrier_upper:
            return R, R, R
        else:
            seed = 1000
            np.random.seed(seed)
    
            # delta t
            deltaT = T/N
            # generate the paths of stock prices
            values = []
            sequencer = qmc.Sobol(d=N, seed=seed)
            # uniform samples
            X = np.array(sequencer.random(n=M))
            # standard normal samples
            Z = norm.ppf(X)
            # scaled samples
            samples = (r - 0.5 * sigma * sigma) * deltaT + \
                sigma * math.sqrt(deltaT) * Z
            df_samples = pd.DataFrame(samples)
            df_samples_cumsum = df_samples.cumsum(axis=1)
            df_stocks = s * np.exp(df_samples_cumsum)
    
            for ipath in df_stocks.index.to_list():
                ds_path_local = df_stocks.loc[ipath, :]
                price_max = ds_path_local.max()
                price_min = ds_path_local.min()
                if price_max >= barrier_upper:  # knock-out happened
                    knockout_time = ds_path_local[ds_path_local >= barrier_upper].index.to_list()[
                        0]
                    payoff = R * np.exp(-knockout_time * r * deltaT)
                    values.append(payoff)
                elif price_min <= barrier_lower:  # knock-in happend
                    final_price = ds_path_local.iloc[-1]
                    payoff = np.exp(- r * T) * max(K - final_price, 0)
                    values.append(payoff)
                else:  # no knock-out, no knock-in
                    values.append(0)
            value = np.mean(values)
            std = np.std(values)
            conf_interval_lower = value - 1.96 * std / math.sqrt(M)
            conf_interval_upper = value + 1.96 * std / math.sqrt(M)
    
            return value, conf_interval_lower, conf_interval_upper

    def verifyinputfcn(self):

        # Objective: verify inputs are correct
        msgtobereturn = []

        # initially assume everything is true
        verifyinput_status = True
        Errorno = 0

        self.optype = self.widget12.currentText()
        self.optionproduct = self.widget11.currentText()

        # collect inputs for checking

        # Spot price of asset S(0) (S1(0) in basket option product)
        try:
            self.S = float(self.widget21.text())
            if (self.S <= 0):
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error " + str(Errorno) + ":spot price S(0) or S1(0) must be a positive real number."))

        except ValueError:
            Errorno = Errorno+1
            msgtobereturn.append(str(
                "Error " + str(Errorno) + ":spot price S(0) or S1(0) must be a positive real number."))

        # strike price K
        try:
            self.K = float(self.widget22.text())
            if (self.K <= 0):
                Errorno = Errorno+1
                msgtobereturn.append(
                    str("Error " + str(Errorno) + ":Strike price K must be a positive real number."))

        except ValueError:
            Errorno = Errorno+1
            msgtobereturn.append(
                str("Error " + str(Errorno) + ":Strike price K must be a positive real number."))

        # Time to maturity T
        try:
            self.T = float(self.widget23.text())
            if (self.T < 0):
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error " + str(Errorno) + ":Time to maturity T must be a non-negative real number."))

        except ValueError:
            Errorno = Errorno+1
            msgtobereturn.append(str(
                "Error " + str(Errorno) + ":Time to maturity T must be a non-negative real number."))

        # interest rate r
        try:
            self.r = float(self.widget24.text())
            if (self.r < 0):
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error " + str(Errorno) + ":interest rate r must be a non-negative real number."))

        except ValueError:
            Errorno = Errorno+1
            msgtobereturn.append(str(
                "Error " + str(Errorno) + ":interest rate r must be a non-negative real number."))

        # sigma of underlying asset (sigma1 in basket option product)
        try:
            if self.optionproduct == "Implied Volatility (European Option)":
                pass
            else:
                self.sigma = float(self.widget25.text())
                if (self.sigma <= 0):
                    Errorno = Errorno+1
                    msgtobereturn.append(
                        str("Error " + str(Errorno) + ":sigma must be a positive real number."))

        except ValueError:
            Errorno = Errorno+1
            msgtobereturn.append(
                str("Error " + str(Errorno) + ":sigma must be a positive real number."))

        if self.optionproduct == "Implied Volatility (European Option)":
            try:
                self.q = float(self.widget28.text())
                if (self.q < 0):
                    Errorno = Errorno+1
                    msgtobereturn.append(
                        str("Error " + str(Errorno) + ":repo rate must be a non-negative real number."))

            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(
                    str("Error " + str(Errorno) + ":repo rate must be a non-negative real number."))

        # additional parameters

        # Option price in getting the implied volatiliy option of vanilla European option.
        if self.optionproduct == 'Implied Volatility (European Option)':
            try:
                self.price = float(self.widget27.text())
                if (self.price < 0):
                    Errorno = Errorno+1
                    msgtobereturn.append(str(
                        "Error " + str(Errorno) + ":option price must be a non-negative real number."))
     
            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error " + str(Errorno) + ":option price must be a non-negative real number."))
        
        '''
        ### check arbirtage condition if there is no error so far
        if (self.optionproduct == 'Implied Volatility (European Option)') & (Errorno==0): 
            self.optype = self.widget12.currentText()
            if self.optype=='Call':
                if 
                
            
            else:
        '''        

        # Repo rate in vanilla European option.
        if self.optionproduct == 'European Option (Closed form)':
            try:
                self.q = float(self.widget28.text())
                if (self.q < 0):
                    Errorno = Errorno+1
                    msgtobereturn.append(
                        str("Error " + str(Errorno) + ":repo rate must be a non-negative real number."))

            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(
                    str("Error " + str(Errorno) + ":repo rate must be a non-negative real number."))

        # No. of  observation steps (tree steps) in KIKO/Asian options (American options).
        if self.optionproduct == 'American Option (Binomial Tree)' or self.optionproduct == 'Geometric Asian Option (Closed form)' or self.optionproduct == 'Asian Option (MC Method)' or self.optionproduct == 'KIKO Put Option (Quasi MC)':
            try:
                self.totsteps = float(self.widget26.text())
                if (self.totsteps <= 0) or (isinstance(self.totsteps, int)) or (self.totsteps>1000):
                    Errorno = Errorno+1
                    if self.optionproduct == 'American Option (Binomial Tree)':
                        msgtobereturn.append(str(
                            "Error "+str(Errorno) + ":No. of steps in tree method must be a positive integer (i.e. n>=1 & n<=1000)."))
                    elif self.optionproduct == 'Geometric Asian Option (Closed form)' or self.optionproduct == 'Asian Option (MC Method)' or self.optionproduct == 'KIKO Put Option (Quasi MC)':
                        msgtobereturn.append(str(
                            "Error "+str(Errorno) + ":No. of observation steps must be a positive integer (i.e. n>=1 & n<=1000)."))

            except ValueError:
                Errorno = Errorno+1
                if self.optionproduct == 'American Option (Binomial Tree)':
                    msgtobereturn.append(str(
                        "Error "+str(Errorno) + ":No. of steps in tree method must be a positive integer (i.e. n>=1 & n<=1000)."))
                elif self.optionproduct == 'Geometric Asian Option (Closed form)' or self.optionproduct == 'Asian Option (MC Method)' or self.optionproduct == 'KIKO Put Option (Quasi MC)':
                    msgtobereturn.append(str(
                        "Error "+str(Errorno) + ":No. of observation steps must be a positive integer (i.e. n>=1 & n<=1000)."))

        # No. of MC paths for all options using monte carlos methods must be >100 and a positive integer
        if self.optionproduct == 'Asian Option (MC Method)' or self.optionproduct == 'Basket Option (2 assets) (MC Method)' or self.optionproduct == 'KIKO Put Option (Quasi MC)':
            try:
                self.M = float(self.widget2MC_1.text())
                if (self.M < 100) or (isinstance(self.M, int)) or (self.M>100000):
                    Errorno = Errorno+1
                    msgtobereturn.append(str(
                        "Error "+str(Errorno) + ":No. of MC simulated paths must be a positive integer (i.e. M>=100 and M<=1e+5)."))
            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error "+str(Errorno) + ":No. of MC simulated paths must be a positive integer (i.e. M>=100 and M<=1e+5)."))

        # paramaters for basket options
        if self.optionproduct == 'Geometric Basket Option (2 assets) (Closed form)' or self.optionproduct == 'Basket Option (2 assets) (MC Method)':
            # S2
            try:
                self.S2 = float(self.widget2bkt_2.text())
                if (self.S2 <= 0):
                    Errorno = Errorno+1
                    msgtobereturn.append(
                        str("Error "+str(Errorno) + ":Spot (S2) must be a positive real number."))
            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(
                    str("Error "+str(Errorno) + ":Spot (S2) must be a positive real number."))

            # Sigma2
            try:
                self.sigma2 = float(self.widget2bkt_4.text())
                if (self.sigma2 <= 0):
                    Errorno = Errorno+1
                    msgtobereturn.append(str(
                        "Error "+str(Errorno) + ":Volatility (sigma2) must be a positive real number."))
            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error "+str(Errorno) + ":Volatility (sigma2) must be a positive real number."))

            # rho
            try:
                self.rho = float(self.widget2bkt_5.text())
                if (self.rho < -1) or (self.rho > 1):
                    Errorno = Errorno+1
                    msgtobereturn.append(str(
                        "Error "+str(Errorno) + ":corelation (rho) must be a real number between -1 and 1."))
            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error "+str(Errorno) + ":corelation (rho) must be a real number between -1 and 1."))

        if self.optionproduct == 'KIKO Put Option (Quasi MC)':
            # lower barrier
            try:
                self.barrier_lower = float(self.widget2KIKO_1.text())
                if (self.barrier_lower <= 0):
                    Errorno = Errorno+1
                    msgtobereturn.append(str(
                        "Error "+str(Errorno) + ":Lower barrier level must be a positive real number."))
            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error "+str(Errorno) + ":Lower barrier level must be a positive real number."))

            # upper barrier
            try:
                self.barrier_upper = float(self.widget2KIKO_2.text())
                if (self.barrier_upper <= 0):
                    Errorno = Errorno+1
                    msgtobereturn.append(str(
                        "Error "+str(Errorno) + ": Upper barrier level must be a positive real number."))
                    # relationship between lower, upper barrier
                else:
                    try:
                        self.barrier_lower = float(self.widget2KIKO_1.text())
                        if (self.barrier_lower >= self.barrier_upper):
                            Errorno = Errorno+1
                            msgtobereturn.append(str(
                                "Error "+str(Errorno) + ": Upper barrier level should be strictly greater than lower barrier level."))
                    except ValueError:
                        pass

            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error "+str(Errorno) + ":Upper barrier level must be a positive real number."))

            # Cash rebate ratio (CR)
            try:
                self.CR = float(self.widget2KIKO_4.text())
                if (self.CR < 0):
                    Errorno = Errorno+1
                    msgtobereturn.append(str(
                        "Error "+str(Errorno)+": Cash rebate (CR) must be a non-negative real number."))

            except ValueError:
                Errorno = Errorno+1
                msgtobereturn.append(str(
                    "Error "+str(Errorno) + ":Cash rebate (CR) must be a non-negative real number."))

        # gather all errors and error statements:
        if (Errorno > 0):
            verifyinput_status = False
        return verifyinput_status,  msgtobereturn
    
    
    def add_line_eu(self, *args, **kwargs):
    #def add_line_eu(self, S,K,sigma,T,r,q,optype,Price):
        row = self.widget41.rowCount()
        self.widget41.setRowCount(row + 1)
        #self.list_parameters = [S,K,sigma,T,r,q,optype,Price]
        # Merge args and kwargs into a single list
        self.list_parameters = list(args) + [value for key, value in kwargs.items()]


        self.col_count = 0
        for p in self.list_parameters:
            if isinstance(p, float):
                self.widget41.setItem(row,self.col_count,QTableWidgetItem(str(round(p,4))))
            else:
                self.widget41.setItem(row,self.col_count,QTableWidgetItem(str(p)))
            self.col_count += 1
        

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
