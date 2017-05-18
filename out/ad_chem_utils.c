#include "header.h"
#include "ad_chem_utils.h"
#include "adept.h"
using adept::adouble;

void eval_conc (const adouble& T, const adouble& pres, const adouble * __restrict__ y, adouble * __restrict__ y_N, adouble * __restrict__ mw_avg, adouble * __restrict__ rho, adouble * __restrict__ conc) {

  // mass fraction of final species
  *y_N = 1.0 - (y[0] + y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7] + y[8]
                + y[9] + y[10] + y[11]);
  *mw_avg = (y[0] * 9.9212254697700253e-01) + (y[1] * 4.9606127348850126e-01)
      + (y[2] * 6.2502343837893923e-02) + (y[3] * 5.8798142449083754e-02)
      + (y[4] * 5.5508435061791990e-02) + (y[5] * 3.1251171918946961e-02)
      + (y[6] * 3.0296842402491128e-02) + (y[7] * 2.9399071224541877e-02)
      + (y[8] * 2.5032542304996495e-02) + (y[9] * 2.4983760555638834e-01)
      + (y[10] * 3.5701025333447579e-02) + (y[11] * 2.2722211870992371e-02) + ((*y_N) * 3.5697100110375433e-02);
  *mw_avg = 1.0 / *mw_avg;
  // mass-averaged density
  *rho = pres * (*mw_avg) / (8.31446210e+03 * T);
  conc[0] = (*rho) * y[0] * 9.9212254697700253e-01;
  conc[1] = (*rho) * y[1] * 4.9606127348850126e-01;
  conc[2] = (*rho) * y[2] * 6.2502343837893923e-02;
  conc[3] = (*rho) * y[3] * 5.8798142449083754e-02;
  conc[4] = (*rho) * y[4] * 5.5508435061791990e-02;
  conc[5] = (*rho) * y[5] * 3.1251171918946961e-02;
  conc[6] = (*rho) * y[6] * 3.0296842402491128e-02;
  conc[7] = (*rho) * y[7] * 2.9399071224541877e-02;
  conc[8] = (*rho) * y[8] * 2.5032542304996495e-02;
  conc[9] = (*rho) * y[9] * 2.4983760555638834e-01;
  conc[10] = (*rho) * y[10] * 3.5701025333447579e-02;
  conc[11] = (*rho) * y[11] * 2.2722211870992371e-02;
  conc[12] = (*rho) * (*y_N) * 3.5697100110375433e-02;

} // end eval_conc

void eval_conc_rho (const adouble& T, const adouble& rho, const adouble * __restrict__ y, adouble * __restrict__ y_N, adouble * __restrict__ mw_avg, adouble * __restrict__ pres, adouble * __restrict__ conc) {

  // mass fraction of final species
  *y_N = 1.0 - (y[0] + y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7] + y[8]
                + y[9] + y[10] + y[11]);
  *mw_avg = (y[0] * 9.9212254697700253e-01) + (y[1] * 4.9606127348850126e-01)
      + (y[2] * 6.2502343837893923e-02) + (y[3] * 5.8798142449083754e-02)
      + (y[4] * 5.5508435061791990e-02) + (y[5] * 3.1251171918946961e-02)
      + (y[6] * 3.0296842402491128e-02) + (y[7] * 2.9399071224541877e-02)
      + (y[8] * 2.5032542304996495e-02) + (y[9] * 2.4983760555638834e-01)
      + (y[10] * 3.5701025333447579e-02) + (y[11] * 2.2722211870992371e-02) + ((*y_N) * 3.5697100110375433e-02);
  *mw_avg = 1.0 / *mw_avg;
  // pressure
  *pres = rho * 8.31446210e+03 * T / (*mw_avg);
  conc[0] = rho * y[0] * 9.9212254697700253e-01;
  conc[1] = rho * y[1] * 4.9606127348850126e-01;
  conc[2] = rho * y[2] * 6.2502343837893923e-02;
  conc[3] = rho * y[3] * 5.8798142449083754e-02;
  conc[4] = rho * y[4] * 5.5508435061791990e-02;
  conc[5] = rho * y[5] * 3.1251171918946961e-02;
  conc[6] = rho * y[6] * 3.0296842402491128e-02;
  conc[7] = rho * y[7] * 2.9399071224541877e-02;
  conc[8] = rho * y[8] * 2.5032542304996495e-02;
  conc[9] = rho * y[9] * 2.4983760555638834e-01;
  conc[10] = rho * y[10] * 3.5701025333447579e-02;
  conc[11] = rho * y[11] * 2.2722211870992371e-02;
  conc[12] = rho * (*y_N) * 3.5697100110375433e-02;

} // end eval_conc

void eval_h (const adouble& T, adouble * __restrict__ h) {

  if (T <= 1000.0) {
    h[0] = 8.2489653153957570e+03 * (2.5471630000000001e+04 + T * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  } else {
    h[0] = 8.2489653153957570e+03 * (2.5471630000000001e+04 + T * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  }

  if (T <= 1000.0) {
    h[1] = 4.1244826576978785e+03 * (-1.0125210000000000e+03 + T * (3.2981240000000001e+00 + T * (4.1247210000000002e-04 + T * (-2.7143383333333332e-07 + T * (-2.3688584999999998e-11 + 8.2697439999999997e-14 * T)))));
  } else {
    h[1] = 4.1244826576978785e+03 * (-8.3503399999999999e+02 + T * (2.9914230000000002e+00 + T * (3.5003220000000003e-04 + T * (-1.8779430000000000e-08 + T * (-2.3078944999999999e-12 + 3.1655040000000001e-16 * T)))));
  }

  if (T <= 1000.0) {
    h[2] = 5.1967336900133762e+02 * (2.9147639999999999e+04 + T * (2.9464290000000002e+00 + T * (-8.1908299999999996e-04 + T * (8.0701066666666660e-07 + T * (-4.0071074999999999e-10 + 7.7813920000000000e-14 * T)))));
  } else {
    h[2] = 5.1967336900133762e+02 * (2.9230799999999999e+04 + T * (2.5420600000000002e+00 + T * (-1.3775310000000001e-05 + T * (-1.0342676666666666e-09 + T * (1.1377667500000001e-12 + -8.7361040000000001e-17 * T)))));
  }

  if (T <= 1000.0) {
    h[3] = 4.8887492694330808e+02 * (3.3463091300000001e+03 + T * (4.1253056099999998e+00 + T * (-1.6127246950000001e-03 + T * (2.1758823033333334e-06 + T * (-1.4496341075000000e-09 + 4.1247475799999997e-13 * T)))));
  } else {
    h[3] = 4.8887492694330808e+02 * (3.6836287499999999e+03 + T * (2.8647288600000000e+00 + T * (5.2825224000000001e-04 + T * (-8.6360919333333338e-08 + T * (7.6304668500000001e-12 + -2.6639175200000000e-16 * T)))));
  }

  if (T <= 1000.0) {
    h[4] = 4.6152277955158070e+02 * (-3.0208110000000001e+04 + T * (3.3868420000000001e+00 + T * (1.7374910000000001e-03 + T * (-2.1182319999999999e-06 + T * (1.7421452500000000e-09 + -5.0131760000000006e-13 * T)))));
  } else {
    h[4] = 4.6152277955158070e+02 * (-2.9899209999999999e+04 + T * (2.6721460000000001e+00 + T * (1.5281464999999999e-03 + T * (-2.9100866666666669e-07 + T * (3.0024900000000001e-11 + -1.2783236000000000e-15 * T)))));
  }

  if (T <= 1000.0) {
    h[5] = 2.5983668450066881e+02 * (-1.0052490000000000e+03 + T * (3.2129360000000000e+00 + T * (5.6374300000000001e-04 + T * (-1.9187166666666667e-07 + T * (3.2846925000000002e-10 + -1.7537108000000000e-13 * T)))));
  } else {
    h[5] = 2.5983668450066881e+02 * (-1.2339300000000001e+03 + T * (3.6975780000000000e+00 + T * (3.0675985000000000e-04 + T * (-4.1961400000000003e-08 + T * (4.4382025000000000e-12 + -2.2728700000000004e-16 * T)))));
  }

  if (T <= 1000.0) {
    h[6] = 2.5190194790518544e+02 * (2.9480804000000001e+02 + T * (4.3017980099999997e+00 + T * (-2.3745602549999998e-03 + T * (7.0527630333333326e-06 + T * (-6.0690973500000000e-09 + 1.8584502480000002e-12 * T)))));
  } else {
    h[6] = 2.5190194790518544e+02 * (1.1185671300000000e+02 + T * (4.0172109000000003e+00 + T * (1.1199100650000000e-03 + T * (-2.1121938333333332e-07 + T * (2.8561592500000001e-11 + -2.1581707000000000e-15 * T)))));
  }

  if (T <= 1000.0) {
    h[7] = 2.4443746347165404e+02 * (-1.7663150000000001e+04 + T * (3.3887540000000000e+00 + T * (3.2846130000000000e-03 + T * (-4.9500433333333328e-08 + T * (-1.1564514999999999e-09 + 4.9430299999999994e-13 * T)))));
  } else {
    h[7] = 2.4443746347165404e+02 * (-1.8006959999999999e+04 + T * (4.5731669999999998e+00 + T * (2.1680680000000000e-03 + T * (-4.9156300000000002e-07 + T * (5.8722599999999994e-11 + -2.8633079999999999e-15 * T)))));
  }

  if (T <= 1000.0) {
    h[8] = 2.0813212426154001e+02 * (-7.4537500000000000e+02 + T * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  } else {
    h[8] = 2.0813212426154001e+02 * (-7.4537500000000000e+02 + T * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  }

  if (T <= 1000.0) {
    h[9] = 2.0772653025533405e+03 * (-7.4537500000000000e+02 + T * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  } else {
    h[9] = 2.0772653025533405e+03 * (-7.4537500000000000e+02 + T * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  }

  if (T <= 1000.0) {
    h[10] = 2.9683482206608977e+02 * (-1.4310540000000001e+04 + T * (3.2624520000000001e+00 + T * (7.5597049999999997e-04 + T * (-1.2939183333333334e-06 + T * (1.3954860000000001e-09 + -4.9499020000000001e-13 * T)))));
  } else {
    h[10] = 2.9683482206608977e+02 * (-1.4268350000000000e+04 + T * (3.0250780000000002e+00 + T * (7.2134450000000002e-04 + T * (-1.8769426666666668e-07 + T * (2.5464525000000000e-11 + -1.3821904000000000e-15 * T)))));
  }

  if (T <= 1000.0) {
    h[11] = 1.8892296942953618e+02 * (-4.8373139999999999e+04 + T * (2.2757250000000000e+00 + T * (4.9610360000000003e-03 + T * (-3.4697033333333334e-06 + T * (1.7166717500000000e-09 + -4.2345600000000001e-13 * T)))));
  } else {
    h[11] = 1.8892296942953618e+02 * (-4.8966959999999999e+04 + T * (4.4536230000000003e+00 + T * (1.5700845000000000e-03 + T * (-4.2613700000000000e-07 + T * (5.9849924999999994e-11 + -3.3380660000000002e-15 * T)))));
  }

  if (T <= 1000.0) {
    h[12] = 2.9680218594762238e+02 * (-1.0209000000000000e+03 + T * (3.2986770000000001e+00 + T * (7.0412000000000003e-04 + T * (-1.3210739999999999e-06 + T * (1.4103787500000001e-09 + -4.8897100000000006e-13 * T)))));
  } else {
    h[12] = 2.9680218594762238e+02 * (-9.2279769999999996e+02 + T * (2.9266399999999999e+00 + T * (7.4398849999999996e-04 + T * (-1.8949203333333333e-07 + T * (2.5242600000000000e-11 + -1.3506701999999999e-15 * T)))));
  }

} // end eval_h

void eval_u (const adouble& T, adouble * __restrict__ u) {

  if (T <= 1000.0) {
    u[0] = 8.2489653153957570e+03 * (2.5471630000000001e+04 + T * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  } else {
    u[0] = 8.2489653153957570e+03 * (2.5471630000000001e+04 + T * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  }

  if (T <= 1000.0) {
    u[1] = 4.1244826576978785e+03 * (-1.0125210000000000e+03 + T * (3.2981240000000001e+00 - 1.0 + T * (4.1247210000000002e-04 + T * (-2.7143383333333332e-07 + T * (-2.3688584999999998e-11 + 8.2697439999999997e-14 * T)))));
  } else {
    u[1] = 4.1244826576978785e+03 * (-8.3503399999999999e+02 + T * (2.9914230000000002e+00 - 1.0 + T * (3.5003220000000003e-04 + T * (-1.8779430000000000e-08 + T * (-2.3078944999999999e-12 + 3.1655040000000001e-16 * T)))));
  }

  if (T <= 1000.0) {
    u[2] = 5.1967336900133762e+02 * (2.9147639999999999e+04 + T * (2.9464290000000002e+00 - 1.0 + T * (-8.1908299999999996e-04 + T * (8.0701066666666660e-07 + T * (-4.0071074999999999e-10 + 7.7813920000000000e-14 * T)))));
  } else {
    u[2] = 5.1967336900133762e+02 * (2.9230799999999999e+04 + T * (2.5420600000000002e+00 - 1.0 + T * (-1.3775310000000001e-05 + T * (-1.0342676666666666e-09 + T * (1.1377667500000001e-12 + -8.7361040000000001e-17 * T)))));
  }

  if (T <= 1000.0) {
    u[3] = 4.8887492694330808e+02 * (3.3463091300000001e+03 + T * (4.1253056099999998e+00 - 1.0 + T * (-1.6127246950000001e-03 + T * (2.1758823033333334e-06 + T * (-1.4496341075000000e-09 + 4.1247475799999997e-13 * T)))));
  } else {
    u[3] = 4.8887492694330808e+02 * (3.6836287499999999e+03 + T * (2.8647288600000000e+00 - 1.0 + T * (5.2825224000000001e-04 + T * (-8.6360919333333338e-08 + T * (7.6304668500000001e-12 + -2.6639175200000000e-16 * T)))));
  }

  if (T <= 1000.0) {
    u[4] = 4.6152277955158070e+02 * (-3.0208110000000001e+04 + T * (3.3868420000000001e+00 - 1.0 + T * (1.7374910000000001e-03 + T * (-2.1182319999999999e-06 + T * (1.7421452500000000e-09 + -5.0131760000000006e-13 * T)))));
  } else {
    u[4] = 4.6152277955158070e+02 * (-2.9899209999999999e+04 + T * (2.6721460000000001e+00 - 1.0 + T * (1.5281464999999999e-03 + T * (-2.9100866666666669e-07 + T * (3.0024900000000001e-11 + -1.2783236000000000e-15 * T)))));
  }

  if (T <= 1000.0) {
    u[5] = 2.5983668450066881e+02 * (-1.0052490000000000e+03 + T * (3.2129360000000000e+00 - 1.0 + T * (5.6374300000000001e-04 + T * (-1.9187166666666667e-07 + T * (3.2846925000000002e-10 + -1.7537108000000000e-13 * T)))));
  } else {
    u[5] = 2.5983668450066881e+02 * (-1.2339300000000001e+03 + T * (3.6975780000000000e+00 - 1.0 + T * (3.0675985000000000e-04 + T * (-4.1961400000000003e-08 + T * (4.4382025000000000e-12 + -2.2728700000000004e-16 * T)))));
  }

  if (T <= 1000.0) {
    u[6] = 2.5190194790518544e+02 * (2.9480804000000001e+02 + T * (4.3017980099999997e+00 - 1.0 + T * (-2.3745602549999998e-03 + T * (7.0527630333333326e-06 + T * (-6.0690973500000000e-09 + 1.8584502480000002e-12 * T)))));
  } else {
    u[6] = 2.5190194790518544e+02 * (1.1185671300000000e+02 + T * (4.0172109000000003e+00 - 1.0 + T * (1.1199100650000000e-03 + T * (-2.1121938333333332e-07 + T * (2.8561592500000001e-11 + -2.1581707000000000e-15 * T)))));
  }

  if (T <= 1000.0) {
    u[7] = 2.4443746347165404e+02 * (-1.7663150000000001e+04 + T * (3.3887540000000000e+00 - 1.0 + T * (3.2846130000000000e-03 + T * (-4.9500433333333328e-08 + T * (-1.1564514999999999e-09 + 4.9430299999999994e-13 * T)))));
  } else {
    u[7] = 2.4443746347165404e+02 * (-1.8006959999999999e+04 + T * (4.5731669999999998e+00 - 1.0 + T * (2.1680680000000000e-03 + T * (-4.9156300000000002e-07 + T * (5.8722599999999994e-11 + -2.8633079999999999e-15 * T)))));
  }

  if (T <= 1000.0) {
    u[8] = 2.0813212426154001e+02 * (-7.4537500000000000e+02 + T * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  } else {
    u[8] = 2.0813212426154001e+02 * (-7.4537500000000000e+02 + T * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  }

  if (T <= 1000.0) {
    u[9] = 2.0772653025533405e+03 * (-7.4537500000000000e+02 + T * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  } else {
    u[9] = 2.0772653025533405e+03 * (-7.4537500000000000e+02 + T * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T)))));
  }

  if (T <= 1000.0) {
    u[10] = 2.9683482206608977e+02 * (-1.4310540000000001e+04 + T * (3.2624520000000001e+00 - 1.0 + T * (7.5597049999999997e-04 + T * (-1.2939183333333334e-06 + T * (1.3954860000000001e-09 + -4.9499020000000001e-13 * T)))));
  } else {
    u[10] = 2.9683482206608977e+02 * (-1.4268350000000000e+04 + T * (3.0250780000000002e+00 - 1.0 + T * (7.2134450000000002e-04 + T * (-1.8769426666666668e-07 + T * (2.5464525000000000e-11 + -1.3821904000000000e-15 * T)))));
  }

  if (T <= 1000.0) {
    u[11] = 1.8892296942953618e+02 * (-4.8373139999999999e+04 + T * (2.2757250000000000e+00 - 1.0 + T * (4.9610360000000003e-03 + T * (-3.4697033333333334e-06 + T * (1.7166717500000000e-09 + -4.2345600000000001e-13 * T)))));
  } else {
    u[11] = 1.8892296942953618e+02 * (-4.8966959999999999e+04 + T * (4.4536230000000003e+00 - 1.0 + T * (1.5700845000000000e-03 + T * (-4.2613700000000000e-07 + T * (5.9849924999999994e-11 + -3.3380660000000002e-15 * T)))));
  }

  if (T <= 1000.0) {
    u[12] = 2.9680218594762238e+02 * (-1.0209000000000000e+03 + T * (3.2986770000000001e+00 - 1.0 + T * (7.0412000000000003e-04 + T * (-1.3210739999999999e-06 + T * (1.4103787500000001e-09 + -4.8897100000000006e-13 * T)))));
  } else {
    u[12] = 2.9680218594762238e+02 * (-9.2279769999999996e+02 + T * (2.9266399999999999e+00 - 1.0 + T * (7.4398849999999996e-04 + T * (-1.8949203333333333e-07 + T * (2.5242600000000000e-11 + -1.3506701999999999e-15 * T)))));
  }

} // end eval_u

void eval_cv (const adouble& T, adouble * __restrict__ cv) {

  if (T <= 1000.0) {
    cv[0] = 8.2489653153957570e+03 * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  } else {
    cv[0] = 8.2489653153957570e+03 * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  }

  if (T <= 1000.0) {
    cv[1] = 4.1244826576978785e+03 * (3.2981240000000001e+00 - 1.0 + T * (8.2494420000000005e-04 + T * (-8.1430150000000002e-07 + T * (-9.4754339999999994e-11 + 4.1348719999999999e-13 * T))));
  } else {
    cv[1] = 4.1244826576978785e+03 * (2.9914230000000002e+00 - 1.0 + T * (7.0006440000000005e-04 + T * (-5.6338289999999998e-08 + T * (-9.2315779999999998e-12 + 1.5827520000000000e-15 * T))));
  }

  if (T <= 1000.0) {
    cv[2] = 5.1967336900133762e+02 * (2.9464290000000002e+00 - 1.0 + T * (-1.6381659999999999e-03 + T * (2.4210319999999998e-06 + T * (-1.6028429999999999e-09 + 3.8906960000000000e-13 * T))));
  } else {
    cv[2] = 5.1967336900133762e+02 * (2.5420600000000002e+00 - 1.0 + T * (-2.7550620000000002e-05 + T * (-3.1028029999999998e-09 + T * (4.5510670000000002e-12 + -4.3680520000000002e-16 * T))));
  }

  if (T <= 1000.0) {
    cv[3] = 4.8887492694330808e+02 * (4.1253056099999998e+00 - 1.0 + T * (-3.2254493900000002e-03 + T * (6.5276469100000001e-06 + T * (-5.7985364300000001e-09 + 2.0623737899999999e-12 * T))));
  } else {
    cv[3] = 4.8887492694330808e+02 * (2.8647288600000000e+00 - 1.0 + T * (1.0565044800000000e-03 + T * (-2.5908275800000001e-07 + T * (3.0521867400000000e-11 + -1.3319587600000001e-15 * T))));
  }

  if (T <= 1000.0) {
    cv[4] = 4.6152277955158070e+02 * (3.3868420000000001e+00 - 1.0 + T * (3.4749820000000002e-03 + T * (-6.3546960000000002e-06 + T * (6.9685809999999998e-09 + -2.5065880000000002e-12 * T))));
  } else {
    cv[4] = 4.6152277955158070e+02 * (2.6721460000000001e+00 - 1.0 + T * (3.0562929999999999e-03 + T * (-8.7302600000000002e-07 + T * (1.2009960000000001e-10 + -6.3916179999999999e-15 * T))));
  }

  if (T <= 1000.0) {
    cv[5] = 2.5983668450066881e+02 * (3.2129360000000000e+00 - 1.0 + T * (1.1274860000000000e-03 + T * (-5.7561500000000004e-07 + T * (1.3138770000000001e-09 + -8.7685540000000003e-13 * T))));
  } else {
    cv[5] = 2.5983668450066881e+02 * (3.6975780000000000e+00 - 1.0 + T * (6.1351970000000000e-04 + T * (-1.2588420000000000e-07 + T * (1.7752810000000000e-11 + -1.1364350000000001e-15 * T))));
  }

  if (T <= 1000.0) {
    cv[6] = 2.5190194790518544e+02 * (4.3017980099999997e+00 - 1.0 + T * (-4.7491205099999996e-03 + T * (2.1158289099999999e-05 + T * (-2.4276389400000000e-08 + 9.2922512400000003e-12 * T))));
  } else {
    cv[6] = 2.5190194790518544e+02 * (4.0172109000000003e+00 - 1.0 + T * (2.2398201299999999e-03 + T * (-6.3365814999999998e-07 + T * (1.1424637000000000e-10 + -1.0790853500000000e-14 * T))));
  }

  if (T <= 1000.0) {
    cv[7] = 2.4443746347165404e+02 * (3.3887540000000000e+00 - 1.0 + T * (6.5692260000000001e-03 + T * (-1.4850129999999999e-07 + T * (-4.6258059999999997e-09 + 2.4715149999999999e-12 * T))));
  } else {
    cv[7] = 2.4443746347165404e+02 * (4.5731669999999998e+00 - 1.0 + T * (4.3361360000000000e-03 + T * (-1.4746890000000000e-06 + T * (2.3489039999999998e-10 + -1.4316540000000001e-14 * T))));
  }

  if (T <= 1000.0) {
    cv[8] = 2.0813212426154001e+02 * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  } else {
    cv[8] = 2.0813212426154001e+02 * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  }

  if (T <= 1000.0) {
    cv[9] = 2.0772653025533405e+03 * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  } else {
    cv[9] = 2.0772653025533405e+03 * (2.5000000000000000e+00 - 1.0 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  }

  if (T <= 1000.0) {
    cv[10] = 2.9683482206608977e+02 * (3.2624520000000001e+00 - 1.0 + T * (1.5119409999999999e-03 + T * (-3.8817550000000001e-06 + T * (5.5819440000000003e-09 + -2.4749509999999998e-12 * T))));
  } else {
    cv[10] = 2.9683482206608977e+02 * (3.0250780000000002e+00 - 1.0 + T * (1.4426890000000000e-03 + T * (-5.6308280000000003e-07 + T * (1.0185810000000000e-10 + -6.9109519999999997e-15 * T))));
  }

  if (T <= 1000.0) {
    cv[11] = 1.8892296942953618e+02 * (2.2757250000000000e+00 - 1.0 + T * (9.9220720000000005e-03 + T * (-1.0409110000000001e-05 + T * (6.8666869999999999e-09 + -2.1172800000000000e-12 * T))));
  } else {
    cv[11] = 1.8892296942953618e+02 * (4.4536230000000003e+00 - 1.0 + T * (3.1401689999999999e-03 + T * (-1.2784110000000000e-06 + T * (2.3939969999999998e-10 + -1.6690330000000000e-14 * T))));
  }

  if (T <= 1000.0) {
    cv[12] = 2.9680218594762238e+02 * (3.2986770000000001e+00 - 1.0 + T * (1.4082400000000001e-03 + T * (-3.9632219999999998e-06 + T * (5.6415150000000002e-09 + -2.4448550000000001e-12 * T))));
  } else {
    cv[12] = 2.9680218594762238e+02 * (2.9266399999999999e+00 - 1.0 + T * (1.4879769999999999e-03 + T * (-5.6847609999999995e-07 + T * (1.0097040000000000e-10 + -6.7533509999999998e-15 * T))));
  }

} // end eval_cv

void eval_cp (const adouble& T, adouble * __restrict__ cp) {

  if (T <= 1000.0) {
    cp[0] = 8.2489653153957570e+03 * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  } else {
    cp[0] = 8.2489653153957570e+03 * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  }

  if (T <= 1000.0) {
    cp[1] = 4.1244826576978785e+03 * (3.2981240000000001e+00 + T * (8.2494420000000005e-04 + T * (-8.1430150000000002e-07 + T * (-9.4754339999999994e-11 + 4.1348719999999999e-13 * T))));
  } else {
    cp[1] = 4.1244826576978785e+03 * (2.9914230000000002e+00 + T * (7.0006440000000005e-04 + T * (-5.6338289999999998e-08 + T * (-9.2315779999999998e-12 + 1.5827520000000000e-15 * T))));
  }

  if (T <= 1000.0) {
    cp[2] = 5.1967336900133762e+02 * (2.9464290000000002e+00 + T * (-1.6381659999999999e-03 + T * (2.4210319999999998e-06 + T * (-1.6028429999999999e-09 + 3.8906960000000000e-13 * T))));
  } else {
    cp[2] = 5.1967336900133762e+02 * (2.5420600000000002e+00 + T * (-2.7550620000000002e-05 + T * (-3.1028029999999998e-09 + T * (4.5510670000000002e-12 + -4.3680520000000002e-16 * T))));
  }

  if (T <= 1000.0) {
    cp[3] = 4.8887492694330808e+02 * (4.1253056099999998e+00 + T * (-3.2254493900000002e-03 + T * (6.5276469100000001e-06 + T * (-5.7985364300000001e-09 + 2.0623737899999999e-12 * T))));
  } else {
    cp[3] = 4.8887492694330808e+02 * (2.8647288600000000e+00 + T * (1.0565044800000000e-03 + T * (-2.5908275800000001e-07 + T * (3.0521867400000000e-11 + -1.3319587600000001e-15 * T))));
  }

  if (T <= 1000.0) {
    cp[4] = 4.6152277955158070e+02 * (3.3868420000000001e+00 + T * (3.4749820000000002e-03 + T * (-6.3546960000000002e-06 + T * (6.9685809999999998e-09 + -2.5065880000000002e-12 * T))));
  } else {
    cp[4] = 4.6152277955158070e+02 * (2.6721460000000001e+00 + T * (3.0562929999999999e-03 + T * (-8.7302600000000002e-07 + T * (1.2009960000000001e-10 + -6.3916179999999999e-15 * T))));
  }

  if (T <= 1000.0) {
    cp[5] = 2.5983668450066881e+02 * (3.2129360000000000e+00 + T * (1.1274860000000000e-03 + T * (-5.7561500000000004e-07 + T * (1.3138770000000001e-09 + -8.7685540000000003e-13 * T))));
  } else {
    cp[5] = 2.5983668450066881e+02 * (3.6975780000000000e+00 + T * (6.1351970000000000e-04 + T * (-1.2588420000000000e-07 + T * (1.7752810000000000e-11 + -1.1364350000000001e-15 * T))));
  }

  if (T <= 1000.0) {
    cp[6] = 2.5190194790518544e+02 * (4.3017980099999997e+00 + T * (-4.7491205099999996e-03 + T * (2.1158289099999999e-05 + T * (-2.4276389400000000e-08 + 9.2922512400000003e-12 * T))));
  } else {
    cp[6] = 2.5190194790518544e+02 * (4.0172109000000003e+00 + T * (2.2398201299999999e-03 + T * (-6.3365814999999998e-07 + T * (1.1424637000000000e-10 + -1.0790853500000000e-14 * T))));
  }

  if (T <= 1000.0) {
    cp[7] = 2.4443746347165404e+02 * (3.3887540000000000e+00 + T * (6.5692260000000001e-03 + T * (-1.4850129999999999e-07 + T * (-4.6258059999999997e-09 + 2.4715149999999999e-12 * T))));
  } else {
    cp[7] = 2.4443746347165404e+02 * (4.5731669999999998e+00 + T * (4.3361360000000000e-03 + T * (-1.4746890000000000e-06 + T * (2.3489039999999998e-10 + -1.4316540000000001e-14 * T))));
  }

  if (T <= 1000.0) {
    cp[8] = 2.0813212426154001e+02 * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  } else {
    cp[8] = 2.0813212426154001e+02 * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  }

  if (T <= 1000.0) {
    cp[9] = 2.0772653025533405e+03 * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  } else {
    cp[9] = 2.0772653025533405e+03 * (2.5000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + T * (0.0000000000000000e+00 + 0.0000000000000000e+00 * T))));
  }

  if (T <= 1000.0) {
    cp[10] = 2.9683482206608977e+02 * (3.2624520000000001e+00 + T * (1.5119409999999999e-03 + T * (-3.8817550000000001e-06 + T * (5.5819440000000003e-09 + -2.4749509999999998e-12 * T))));
  } else {
    cp[10] = 2.9683482206608977e+02 * (3.0250780000000002e+00 + T * (1.4426890000000000e-03 + T * (-5.6308280000000003e-07 + T * (1.0185810000000000e-10 + -6.9109519999999997e-15 * T))));
  }

  if (T <= 1000.0) {
    cp[11] = 1.8892296942953618e+02 * (2.2757250000000000e+00 + T * (9.9220720000000005e-03 + T * (-1.0409110000000001e-05 + T * (6.8666869999999999e-09 + -2.1172800000000000e-12 * T))));
  } else {
    cp[11] = 1.8892296942953618e+02 * (4.4536230000000003e+00 + T * (3.1401689999999999e-03 + T * (-1.2784110000000000e-06 + T * (2.3939969999999998e-10 + -1.6690330000000000e-14 * T))));
  }

  if (T <= 1000.0) {
    cp[12] = 2.9680218594762238e+02 * (3.2986770000000001e+00 + T * (1.4082400000000001e-03 + T * (-3.9632219999999998e-06 + T * (5.6415150000000002e-09 + -2.4448550000000001e-12 * T))));
  } else {
    cp[12] = 2.9680218594762238e+02 * (2.9266399999999999e+00 + T * (1.4879769999999999e-03 + T * (-5.6847609999999995e-07 + T * (1.0097040000000000e-10 + -6.7533509999999998e-15 * T))));
  }

} // end eval_cp
