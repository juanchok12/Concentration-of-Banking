const data = [{
    id: '0.0',
    parent: '',
    name: 'Giga Banks'
  },

  //2nd Level-The Big Four
  {
    id: '1.1',
    parent: '0.0',
    name: 'Chase',
    color: '#0D5EAF' //Blue
  },
  {
    id: '1.2',
    parent: '0.0',
    name: 'Bank of America',
    color: '#CB0D1F' //Red
  },
  {
    id: '1.3',
    parent: '0.0',
    name: 'Wells Fargo',
    color: '#FFD408' //Yellow
  },
  {
    id: '1.4',
    parent: '0.0',
    name: 'Citibank',
    color: '#1598C3' //Yellow
  },

  /* 3rd Level- Chase M&A */

  {
    id: '2.1',
    parent: '1.1',
    name: 'Chemical Bank',
    Amount: '$10B',
    Year: 1996,
    Type: 'Merger-Chemical Bank acquired Chase Manhattan, but it adopted the name Chase'
  },

  {
    id: '2.2',
    parent: '1.1',
    name: 'J.P. Morgan & Co.',
    Amount: '$30.9B',
    Year: 2000,
    Type: 'Merger-Chase Manhattan acquired J.P. Morgan, adopting the name JP Morgan Chase'

  },
  {
    id: '2.3',
    parent: '1.1',
    name: 'Bank One',
    Amount: '$59B',
    Year: 2004,
    Type: 'Merger'
  },

  {
    id: '2.4',
    parent: '1.1',
    name: 'Bear Stearns',
    Amount: '$1.2B',
    Year: 2008,
    Type: 'Acquisition'
  },

  {
    id: '2.5',
    parent: '1.1',
    name: 'Washington Mutual',
    Amount: '$1.9B',
    Year: 2008,
    Type: 'Acquisition'
  },

  {
    id: '2.6',
    parent: '1.1',
    name: 'First Republic Bank',
    Amount: '$10.6B',
    Year: 2023,
    Type: 'Acquisition'
  },





  /* 3rd Level- Bank of America M&A */

  {
    id: '2.7',
    parent: '1.2',
    name: 'FleetBoston',
    Amount: '$47B',
    Year: 2004,
    Type: 'Acquisition'
  },

  {
    id: '2.7',
    parent: '1.2',
    name: 'NationsBank',
    Amount: '$62B',
    Year: 1998,
    Type: 'Merger-Aquisition of BankAmerica by NationsBank,<br> adopting the Bank of America name.<br> At the time, it was the biggest bank acquisition in history'
  },

  {
    id: '2.7',
    parent: '1.2',
    name: 'FleetBoston',
    Amount: '$47B',
    Year: 2004,
    Type: 'Acquisition'
  },

  {
    id: '2.8',
    parent: '1.2',
    name: 'NBNA',
    Amount: '$35B',
    Year: 2006,
    Type: 'Acquisition'
  },

  {
    id: '2.9',
    parent: '1.2',
    name: 'US Trust',
    Amount: '$3.3B',
    Year: 2006,
    Type: 'Acquisition'
  },

  {
    id: '2.10',
    parent: '1.2',
    name: 'Countrywide Financial',
    Amount: '$4B',
    Year: 2008,
    Type: 'Acquisition'
  },

  {
    id: '2.11',
    parent: '1.2',
    name: 'Merril Lynch',
    Amount: '$50B',
    Year: 2009,
    Type: 'Acquisition'
  },

  /* 3rd Level-Wells Fargo M&A */

  {
    id: '2.12',
    parent: '1.3',
    name: 'Great American Bank',
    Amount: '$491M',
    Year: 1996,
    Type: 'Branch consolidation-take over of 130 branches from Great American Bank in California'
  },


  {
    id: '2.13',
    parent: '1.3',
    name: 'First Interstate Bancorp',
    Amount: '$11.6B',
    Year: 1996,
    Type: 'Acquisition'
  },

  {
    id: '2.13',
    parent: '1.3',
    name: 'Norwest Corporation',
    Amount: '$34B',
    Year: 1998,
    Type: 'Merger-Norwest Corporation acquires Wells Fargo Bank to create Wells Fargo '
  },

  {
    id: '2.14',
    parent: '1.3',
    name: 'First Secuirty Corporation',
    Amount: '$2.1B',
    Year: 2000,
    Type: 'Acquisition'
  },

  {
    id: '2.15',
    parent: '1.3',
    name: 'National Bank of Alaska',
    Amount: '$907M',
    Year: 2000,
    Type: 'Acquisition'
  },

  {
    id: '2.16',
    parent: '1.3',
    name: 'Placer Sierra Bank',
    Amount: '$645M',
    Year: 2007,
    Type: 'Acquisition'
  },

  {
    id: '2.17',
    parent: '1.3',
    name: 'Greater Bay Bancorp',
    Amount: '$1.5B',
    Year: 2007,
    Type: 'Acquisition'
  },

  {
    id: '2.18',
    parent: '1.3',
    name: 'United Bancorp',
    Amount: '$760M',
    Year: 2008,
    Type: 'Acquisition'
  },

  {
    id: '2.19',
    parent: '1.3',
    name: 'Wachovia',
    Amount: '$14.8B',
    Year: 2008,
    Type: 'Acquisition'
  },



  /* 3rd Level-Citigroup M&A */


  {
    id: '2.16',
    parent: '1.4',
    name: 'Travelers Group',
    Amount: '$70B',
    Year: 1998,
    Type: 'Merger-Citicorp and Trevelers Group combined to create Citigroup,<br> making the transfomration the largest merger ever at the time in US history.'
  },

  {
    id: '2.17',
    parent: '1.4',
    name: 'Associates First Capital Corp.',
    Amount: '$31.1B',
    Year: 2000,
    Type: 'Acquisition'
  },

  {
    id: '2.18',
    parent: '1.4',
    name: 'European American Bank',
    Amount: '$1.9B',
    Year: 2001,
    Type: 'Acquisition'
  },

  {
    id: '2.18',
    parent: '1.4',
    name: 'Banamex',
    Amount: '$12.5B',
    Year: 2001,
    Type: 'Acquisition-second largest US bank foreign investment'
  },

  {
    id: '2.18',
    parent: '1.4',
    name: 'St. Paul Companies',
    Amount: '$16B',
    Year: 2002,
    Type: 'Merger-Travelers, a subsidiary of Citigroup, merged with St. Paul Companies to create St. Paul Travelers<br> (now known as Travelers Companies Inc.), the second largest writer of US commercial property casualty insurance.'
  },


  /* Oceania */


];

Highcharts.chart('container', {

  chart: {
    backgroundColor: '#121212', // Dark background
    plotBackgroundColor: '#121212',
    inverted: false,
    marginBottom: 170,
    spacingBottom: 30,
    marginRight: 120,
    height: 1200,

    /*       borderWidth: 0,
                  borderColor: '#121212',
          plotBorderWidth: 0,
                  plotBorderColor: '#121212' */
  },
  title: {
    text: 'Phylogenetic Tree of Mergers and Acquisitions of the Big Four Banks',
    align: 'center',
    style: {
      color: '#FFFFFF'
    }
  },





  tooltip: {
    formatter: function() {
      // 'this' context refers to the tooltip
      // You can access the current point using this.point
      return this.point.name + '</b><br>' +
        'Amount: ' + this.point.Amount + '<br>' +
        'Year: ' + this.point.Year + '<br>' +
        'Type: ' + this.point.Type;
    }
  },

  series: [{
    type: 'treegraph',
    data,
    tooltip: {
      pointFormat: '{point.name}'
    },
    dataLabels: {
      pointFormat: '{point.name}',
      style: {
        whiteSpace: 'nowrap',
        color: '#FFFFFF',
        textOutline: '3px contrast'
      },
      crop: false
    },
    marker: {
      radius: 6,
      lineColor: '#FFFFFF',
      lineWidth: 0.5
    },
    levels: [{
        level: 1,
        dataLabels: {
          align: 'left',
          x: 20
        }
      },
      {
        level: 2,
        colorByPoint: true,
        dataLabels: {
          verticalAlign: 'bottom',
          y: -20
        }
      },
      {
        level: 3,
        colorVariation: {
          key: 'brightness',
          to: -0.5
        },
        dataLabels: {
          verticalAlign: 'bottom',
          rotation: 0,
          y: 20,
          x: 0,
        }
      },
      {
        level: 4,
        colorVariation: {
          key: 'brightness',
          to: -0.5
        },
        dataLabels: {
          verticalAlign: 'top',
          rotation: 0,
          y: 10,
          x: 0,
          crop: false,
          rotation: 0,
          overflow: 'allow'

        }
      },

    ]
  }]
});
